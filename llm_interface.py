import requests
import json

DOLPHIN_MODEL = "dolphin-2.8-mistral-7b-v02"
GEMMA_MODEL = "gemma-3-12b-it"
BASE_URL = "http://localhost:1234/v1/chat/completions"

with open("llm_config.json") as f:
    config = json.load(f)

def send_message(model, message, temperature=0.7, system_prompt = ""):
    """Send a message and receive a response using the chat endpoint."""
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
            ],
        "temperature": temperature,
    }
    response = requests.post(BASE_URL, json=data)
    
    if response.ok:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def generate_story():
    return send_message(DOLPHIN_MODEL, config.get("main_prompt"))

def generate_prompts(story):
    return send_message(GEMMA_MODEL, config.get("image_prompt") + story, system_prompt=config.get("system_prompt"))

def generate_title(story):
    return send_message(DOLPHIN_MODEL, story + "\n\n" + config.get("title_prompt"))

if __name__ == "__main__":
    with open("temp/story.txt") as f:
        print(generate_prompts(f.read()))