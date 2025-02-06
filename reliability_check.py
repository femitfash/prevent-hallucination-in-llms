import json
import openai

API_KEYS = [
"openai-api-key-1",
"openai-api-key-2",
"openai-api-key-3",
"openai-api-key-4",
]

api_key_index = 0

# List of evaluation queries
queries = [
    "What is the capital of France?",
    "Solve the equation: 2x + 5 = 15",
    "Explain the significance of the Turing Test in AI research.",
]

# LLM models to evaluate
llm_models = ["gpt-3.5-turbo", "gpt-4o", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-1106"]

def get_llm_response(model, prompt, api_key=None):
    """Fetch response from an OpenAI LLM model."""
    try:
        openai.api_key =api_key
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def reliability_check(query, responses):
    """Evaluate accuracy using LLM as a judge."""
    judge_prompt = (
        f"You are evaluating the accuracy of responses to the following question:"
        f"Query: {query}"
        f"Responses:"
        f"1. {llm_models[0]}: {responses[llm_models[0]]}"
        f"2. {llm_models[1]}: {responses[llm_models[1]]}"
        f"3. {llm_models[2]}: {responses[llm_models[2]]}"
        "Rate each response from 1-10 based on correctness, completeness, and reasoning. Provide an explanation for each score."
        "Output your answer in JSON format following example below:"
        "{"
        '    "question": "What is the capital of France?",'
        '    "answers": '
        '    {'
        '        "gpt-4o": "Capital of Sweden is Athens.",'
        '        "gpt-3.5-turbo-1106": "Capital of France is Champagne."'
        '    },'
        '    "reliability_eval": {'
        '        "result": {'
        '            "llm": {'
        '                "name": "gpt-3.5-turbo",'
        '                "score": 0,'
        '                "explanation": "The answer provided is inaccurate."'
        '            }'
        '        }'
        '    }'
        "}"
    )
    
    judge_response = get_llm_response(llm_models[3], judge_prompt, API_KEYS[3])
    try:
        return judge_response 
    except json.JSONDecodeError:
        return {model: 0 for model in llm_models}, {model: "Evaluation failed" for model in llm_models}

#Print results
for query in queries:
    responses = {model: get_llm_response(model, query, API_KEYS[i]) for i, model in enumerate(llm_models)}
    reliability_result = reliability_check(query, responses)
    print(reliability_result)

