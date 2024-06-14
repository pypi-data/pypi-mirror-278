import requests

url = "https://api-b2b.backenster.com/b1/api/v3/translate"

payload = {
    "platform": "api",
    "from": "en_GB",
    "to": "de_DE",
    "data": "Some text",
    "enableTransliteration": True,
    "translateMode": "html"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": ""
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)