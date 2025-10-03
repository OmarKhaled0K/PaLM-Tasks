from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import time
from collections import Counter
from eval import Evaluator

def extract_answer(text):
    """Extract text between <answer> and </answer> tags.
    Args: text (str) the output text of LLM (the completion)
    Returns: the final answer which is between the `answer` tags or empty string if not found
    """
    start_tag = "<answer>"
    end_tag = "</answer>"
    
    try:
        start_pos = text.index(start_tag) + len(start_tag)
        end_pos = text.index(end_tag)
        return text[start_pos:end_pos]
    except ValueError:
        return ""

def call_model(prompt,llm, model_name="gpt-4.1-mini", temperature=0.5):
    """Call the language model and extract the answer from response.
    Args: prompt (str): the input prompt to the model
            llm : an instance of OpenAI client
           model_name (str): the model name to be used ( default "gpt-4.1-mini" )
           temperature (float): the temperature of the model ( default 0.5 )
    Returns: the final answer which is between the `answer` tags or empty string if not found
           """
    resp = llm.chat.completions.create(
        model=model_name,
        messages=[{"role":"user","content":prompt}],
        temperature=temperature,
        max_tokens=600
    )
    raw_output = resp.choices[0].message.content.strip()
    final_answer = extract_answer(raw_output)
    return final_answer

def run_harness(cases_file,llm, n_runs=5, output_file=None):
    """
    1. Load test cases from JSON file
    2. For each test case, run the prompt for n times
    3. Collect responses, latencies
    4. Compute consistency metrics
    5. Evaluate each response vs expected according to match_type
    6. Summarize results and write to output file if given
    Args:
        cases_file (str): path to JSON file with test cases
        llm: an instance of OpenAI client
        n_runs (int): number of times to run each prompt
        output_file (str): path to write results JSON (if None, don't write)
    Returns: dict with summary and detailed results
    """
    with open(cases_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    evaluator = Evaluator()
    results = []
    summary = {"cases": 0, "total_runs": 0, "passes": 0}

    for test_case in cases:
        case_id = test_case.get("id")
        prompts = [test_case.get("prompt")] + test_case.get("variants", [])
        all_responses = []
        per_prompt_records = []

        for prompt in prompts:
            p_responses = []
            latencies = []
            for i in range(n_runs):
                t0 = time.time()
                try:
                    resp = call_model(prompt,llm, temperature=0.5)
                    print(f"[{case_id}] Run {i+1}/{n_runs} (live): {resp}")
                except Exception as e:
                    resp = f"[ERROR_CALL_MODEL] {e}"
                dt = time.time() - t0
                p_responses.append(resp)
                latencies.append(dt)
            per_prompt_records.append({"prompt": prompt, "responses": p_responses, "latencies": latencies})
            all_responses.extend(p_responses)
        
        # compute consistency metrics
        freq = Counter(all_responses)
        mode_resp, mode_count = freq.most_common(1)[0] if freq else ("", 0)
        consistency = mode_count / (len(all_responses) if all_responses else 1)
        unique_outputs = len(freq)

        # evaluate each response vs expected according to match_type
        pass_count = 0
        details = []
        for resp in all_responses:
            ok, meta = evaluator.evaluate_response(resp, test_case)
            pass_count += 1 if ok else 0
            details.append({"response": resp, "pass": ok, "meta": meta})

        pass_rate = pass_count / (len(all_responses) if all_responses else 1)
        avg_latency = sum([lt for pr in per_prompt_records for lt in pr["latencies"]]) / (len(per_prompt_records)*n_runs if per_prompt_records else 1)

        result_case = {
            "id": case_id,
            "title": test_case.get("title"),
            "type": test_case.get("type"),
            "num_prompts_tested": len(prompts),
            "num_runs_total": len(all_responses),
            "unique_outputs": unique_outputs,
            "mode_response": mode_resp,
            "mode_count": mode_count,
            "consistency": consistency,
            "pass_rate": pass_rate,
            "avg_latency_s": avg_latency,
            "per_prompt": per_prompt_records,
            "details": details
        }
        results.append(result_case)

        summary["cases"] += 1
        summary["total_runs"] += len(all_responses)
        summary["passes"] += pass_count

        print(f"[{case_id}] runs={len(all_responses)} unique={unique_outputs} consistency={consistency:.2f} pass_rate={pass_rate:.2f} avg_latency={avg_latency:.3f}s")

    summary["overall_pass_rate"] = summary["passes"] / summary["total_runs"] if summary["total_runs"] else 0.0
    print("\nSUMMARY:")
    print(json.dumps(summary, indent=2))
    out = {"summary": summary, "results": results}
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print("Wrote results to", output_file)
    return out

if __name__ == "__main__":
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    n_runs = 2
    cases_file = "test_cases.json"
    llm = OpenAI(api_key=api_key)
    output_file = "results.json"
    run_harness(cases_file,llm=llm, n_runs=n_runs,  output_file=output_file)
