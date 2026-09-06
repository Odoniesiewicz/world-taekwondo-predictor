import requests

URL = "https://results.worldtaekwondo.org/competitions/2024-paris-olympic-games/results"

response = requests.get(URL)
print(response.status_code)
print(len(response.text))
print(response.text[:500])
