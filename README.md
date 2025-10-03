# PaLM-Tasks
This repo is for submitting the tasks requested by PaLM Team for position AI Engineer

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
    2. 
- Draft:
    - Maybe you should enclude the GTA idea in your prompt template as a bonus 
    - Prompt cases : 

        - Synthetic:
            1. Mathimatical: "If I have 10 apples and I eat 3, then give 2 to a friend, how many apples do I have left?", The answer must be "5"
            2. Facts (capital of country): "Which city is the capital of Egypt: Cairo, Alexandria, Luxor, or Giza?", The answer must be "Cairo" 
            3. Yes/No Consistency: "Is water dry?"
            4. Facts: "Reverse the word 'DontEverRverseMe'" Then answer must be 'eMesrevRrevEtnoD' ( I know that reverse missing 'e')
            5. Facts: "Which is heavier: an elephant or a mouse?" The answer must be "Elephant"
        - Real-world:
            6. SQL: "Table: Employees (id INT, name TEXT, department TEXT, salary INT). Write an SQL query to find the highest salary in each department.\n Don't return any additional text, only the query", The answer must be executable SQL query return right answer
            7. Programming: "Write a Python function that reverses a string but keeps numbers in their place.", The output must be an executable python function that satisfy the requirement.\n Don't return any additional text, only the function . 
            8. Reasoning (small): "A bat and a ball cost $1.10 in total. The bat costs $1 more than the ball. How much does the ball cost?", The answer must be "0.05$"
            9. Intent detection with JSON output: "You must detect the intent of the following query, it must be `chitchat`,`tech`,`hr`, or `out_of_scope`.\nReturn the output in JSON with field `intent` and the intent.\nThe query: 'Hello, How are you?'\n Answer : ```json". The answer must be {"intent": "chitchat"}
            10. user preferences extract: "For the following query, extract any user preferences in JSON with key `user_preferences` and value list of each preference name and its value \n The query :'My name is Omar Khaled, I'm 25 and I work as GenAI Engineer'\n The answer: ```json" The response should be {"user_preferences": ["name":"Omar Khaled", "age": "25","work":"GenAI Engineer"]}
