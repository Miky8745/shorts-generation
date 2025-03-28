import requests
import json

DEFAULT_HOST = "http://127.0.0.1:8888"

def text2img(params: dict) -> dict:
    """
    text to image
    """
    result = requests.post(url=f"{DEFAULT_HOST}/v1/generation/text-to-image",
                           data=json.dumps(params),
                           headers={"Content-Type": "application/json"})
    return result.json()

def generate_image(prompt):

	return text2img({
    	"prompt": prompt,
    	"style_selections": ["Fooocus V2", "Fooocus Enhance", "Fooocus Sharp"],
    	"performance_selection": "Speed",
    	"aspect_ratios_selection": "540*960",
    })[0].get("url")

def download_image(url : str, path_to_file : str):
    response = requests.get(url)
    with open(path_to_file, "wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    url = generate_image("2. Young girl, distressed expression, bird struggling underwater, current.")
    download_image(url, "test.png")