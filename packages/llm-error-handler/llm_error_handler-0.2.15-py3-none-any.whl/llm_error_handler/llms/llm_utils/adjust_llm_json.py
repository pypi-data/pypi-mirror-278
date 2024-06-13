import json
import logging

def adjust_llm_json(llm_json: str) -> dict:
    content = delete_code_block("json",llm_json)
    try:
        llm_response = json.loads(content)
    except Exception as e:
        logging.error(f"Error: {e}")
        llm_response = {}
    
    return llm_response

def delete_code_block(language: str, text: str) -> str:
    return text.replace(f"```{language}", "").replace("```", "")

