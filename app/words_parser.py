import requests
import json
from config import YANDEX_API_KEY


def translate(q: str, source: str, target: str):
    """
    Calls API and returns result in simplified Python dictionary
    """
    url = f"https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={YANDEX_API_KEY}&lang={source}-{target}&text={q}"
    headers = {
        'content-type': "application/json; charset=utf-8",
    }
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    dictionary = data['def']
    if len(dictionary) == 0:
        return None
    else:
        simplified = {'word': dictionary[0]['text'], 'translate': dictionary[0]['tr'][0]['text'],
                      'examples': dictionary[0]['tr'][0]['ex']}
        return simplified
