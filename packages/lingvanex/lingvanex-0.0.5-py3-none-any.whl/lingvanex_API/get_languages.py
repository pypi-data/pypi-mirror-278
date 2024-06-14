import requests

url = "https://api-b2b.backenster.com/b1/api/v3/getLanguages?platform=api"

headers = {
    "accept": "application/json",
    "Authorization": ""
}

response = requests.get(url, headers=headers)

print(response.text)