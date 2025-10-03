# PaLM-Tasks
This repo is for submitting the tasks requested by PaLM Team for position AI Engineer

## Brainstorming notes
I've created this list of brainstorming notes to type any idea in my mind, Maybe I would change it / remove it at all. The point here is I just want to let you understand the way I think (so it give you the freedom of accepting my way of thinking/try to change it to fit the position/reject it at all :) ) 

### Question 1 
1. Task breaking down:
    - Prompt Reliability: When you ask the model (LM) a question, then ask the same question with minor changes, the response must be the same (not really identical but the same direction). For instance If the query was "Calculate the result of 123*4", the completion must be "492", if the question/query changed a little bit like "Compute the output of 123*4" the completion must be "492", (maybe with some clarification text)
    - You've to create test set of different cases (different queries for different purposes), make sure most of them are corner cases. 
    - Include `invariance test` like Paraphrase, Typos or Noise.
    - Include `perturbation test` like distractor, context change.
    - Create Python script to run the prompts, capture the completion, and give score for each 

2. Draft:
    - Maybe you should enclude the GTA idea in your prompt template as a bonus 