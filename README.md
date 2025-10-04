# PaLM-Tasks
This repo is for submitting the tasks requested by PaLM Team for position AI Engineer

## To test the project
- Question 1:
    - `git clone https://github.com/OmarKhaled0K/PaLM-Tasks.git`
    - `cd PaLM-Tasks`
    - `pip install -r requirements.txt`
    - `cd question_1`
    - `python run script.py`

    You will see results in terminal as well as `results.json` file
- Question 2:
    - `git clone https://github.com/OmarKhaled0K/PaLM-Tasks.git`
    - `cd PaLM-Tasks`
    - `pip install -r requirements.txt`
    - `cd question_2`
    - `uvicorn app:app --reload`

    Then, test the endpoints using APIdog, Postman, or even swagger (recommended)
    
    To use swagger, Open `http://127.0.0.1:8000/docs#/` 



## Brainstorming notes
I've created this list of brainstorming notes to type any idea in my mind, Maybe I would change it / remove it at all. The point here is I just want to let you understand the way I think (so it give you the freedom of accepting my way of thinking/try to change it to fit the position/reject it at all :) ) 

### Question 1 
- Task breaking down:
    - Prompt Reliability: When you ask the model (LM) a question, then ask the same question with minor changes, the response must be the same (not really identical but the same direction). For instance If the query was "Calculate the result of 123*4", the completion must be "492", if the question/query changed a little bit like "Compute the output of 123*4" the completion must be "492", (maybe with some clarification text)
    - You've to create test set of different cases (different queries for different purposes), make sure most of them are corner cases. 
    - Include `invariance test` like Paraphrase, Typos or Noise.
    - Include `perturbation test` like distractor, context change.
    - Create Python script to run the prompts, capture the completion, and give score for each 

- For Synthetic cases, The generation rules:
    1. SYN-01 (math): deterministic numbers, no ambiguity. (no paraphrase needed)
    2. SYN-02 (capital invariance): generate variance for factual question
    3. SYN-03 (yes/no): Generate variance of binary question
    4. SYN-04 (perturbation): create distractor paragraphs (2–5 sentences of neutral content) and prefix them to canonical prompt
- Draft:
    - Maybe you should enclude the GTA idea in your prompt template as a bonus 
    - Prompt cases : 

        - Synthetic:
            1. Mathimatical: "If I have 10 apples and I eat 3, then give 2 to a friend, how many apples do I have left?", The answer must be "5"
            2. Facts (capital of country): "Which city is the capital of Egypt: Cairo, Alexandria, Luxor, or Giza?", The answer must be "Cairo" 
            3. Yes/No Consistency: "Is water dry?"
            4. Facts: "Which is heavier: an elephant or a mouse?" The answer must be "Elephant"
        - Real-world:
            5. SQL: "Table: Employees (id INT, name TEXT, department TEXT, salary INT). Write an SQL query to find the highest salary in each department.\n Don't return any additional text, only the query", The answer must be executable SQL query return right answer
            
            6. Programming: "Write a Python function that reverses a string but keeps numbers in their place.", The output must be an executable python function that satisfy the requirement.\n Don't return any additional text, only the function . 
            
            7. Reasoning (small): "A bat and a ball cost $1.10 in total. The bat costs $1 more than the ball. How much does the ball cost?", The answer must be "0.05$"
            
            8. Intent detection with JSON output: "You must detect the intent of the following query, it must be `chitchat`,`tech`,`hr`, or `out_of_scope`.\nReturn the output in JSON with field `intent` and the intent.\nThe query: 'Hello, How are you?'\n Answer : ```json". The answer must be {"intent": "chitchat"}
            
            9. user preferences extract: "For the following query, extract any user preferences in JSON with key `user_preferences` and value list of each preference name and its value \n The query :'My name is Omar Khaled, I'm 25 and I work as GenAI Engineer'\n The answer: ```json" The response should be {"user_preferences": {"name":"Omar Khaled", "age": "25","work":"GenAI Engineer"}}
    
    - I used Claude sonnet 3.5 to review my code (NOT TYPE IT), also I used autocompletion when I typed the docstring
    - I used OpenAI GPT 5 to discuss about the task to be sure that I fully understand it 

- **Shipment plan**:
    1. [DONE] Synthetic test set
    2. [DONE] Real-world test set
    3. [DONE] Invariance/perturbation sets
    4. [DONE] Eval class (exact, sql, and json)
    5. [DONE] Runnable script to run the cases and give scores
    6. [NOT-YET] Add more test data with different types like semantic, code, reasoning, .etc.
    7. [NOT-YET] Add different eval class like semantic, codes, more reasoning, .etc.
    8. [NOT-YET] Use different metrics to check model understanding and relavence of generated answer ( maybe the generated answer is not exact as expected but close to it)
    9. [NOT-YET] Monitor the latency with better way not just time, I think I used `instrumentator` of `FastAPI` once to let me understand the details of time for each method.

- To run question 1 :
    1. add `OPENAI_API_KEY` in .env file
    2. `cd question_01`
    3. run `python run script.y`
    4. Results are saved in `results.json` 
     

### Question 2
- Task brainstorming:
    - I've to build simple retriever, I will build both bm25 and vector retriever and maybe I will include the hybrid
    - Build text corpus to be the data that the retriever retrieve from
    - Build `/answer` endpoint to retrieve the top chunk and concider it the response (as we don't want to use LLM now)
    - Retrieve also top_k of chunks
    - As a bonus, I will build bm25, vector, hybrid endpoints
    - For two index config, I think I will make it bm25 vs vector or hybrid as well as cosine vs dot , as we don't use LLMs so top-k is not necessary
    - I asked GPT to create a denylist for me, I also took sometime to master prometheus more as I used it just once.


