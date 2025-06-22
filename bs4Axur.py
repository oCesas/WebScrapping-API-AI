import requests, re, base64, os
from bs4 import BeautifulSoup
from pathlib import Path
from dotenv import load_dotenv


#Load token
def load_token() -> str:
    return "P4zmcXlJP5XqQQ1naQCb5WSj4NJJzngf" 
    #It could be in a variable of environment (.env), but I can not send 2 files, not even winrar


#First Step of the scrapping
def search_html(url: str) -> str:
    resp_request = requests.get(url)
    resp_request.raise_for_status()
    return resp_request.text

#Extract the image using REGEX and treating the string
def extract_base64_image(html_axur: str) -> bytes:
    soup = BeautifulSoup(html_axur, "lxml")
    tag = soup.find("img", src=re.compile(r"^data:image/"))
    if not tag:
        raise RuntimeError("No image found")
    _, b64_data = tag["src"].split(",", 1)
    return base64.b64decode(b64_data)

#Saving the image, more info inside main()
def save_image(image_bytes: bytes, output_path: Path):
    output_path.write_bytes(image_bytes)

#Enconding again to send to the model
def encode_image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

#Structuring JSON payload
def build_payload(model: str, prompt: str, b64_image: str) -> dict:
    return {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}"
                        }
                    }
                ],
            }
        ]
    }

#Request to the model
def call_model_api(call_model_api_url: str, payload: dict, headers_callmodel: dict) -> dict:
    resp_request = requests.post(call_model_api_url, json=payload, headers=headers_callmodel, timeout=30)
    #resp_request.raise_for_status()
    return resp_request.json()

#Submit to the model
def submit_response(submit_url: str, data_submit: dict, headers_submit: dict):
    resp_request = requests.post(submit_url, json=data_submit, headers=headers_submit, timeout=30)
    resp_request.raise_for_status()

#Main---------------------------------------------------------------
def main():
    #Variables 
    url_page="https://intern.aiaxuropenings.com/scrape/aa9eaf6d-c058-494f-8861-c29ce62d9cc0"
    url_openai_api="https://intern.aiaxuropenings.com/v1/chat/completions"
    url_submit="https://intern.aiaxuropenings.com/api/submit-response"
    model="microsoft-florence-2-large"
    prompt="<DETAILED_CAPTION>"
    axur_image_scrapping = Path("scraped_image.jpg")

    token = load_token()
    headers_callmodel = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    #Functions/Metods 
    html_axur = search_html(url_page)
    image_bytes = extract_base64_image(html_axur)
    save_image(image_bytes, axur_image_scrapping)
    b64_image = encode_image_to_base64(axur_image_scrapping)

    payload = build_payload(model, prompt, b64_image)
    response_json = call_model_api(url_openai_api, payload, headers_callmodel)
    print("Model resp_request:", response_json)

    submit_response(url_submit, response_json, headers_callmodel)

if __name__ == "__main__":
    main()
