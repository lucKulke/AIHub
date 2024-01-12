import requests
import json


class Dalle:
    def __init__(self, key):
        self.api_key = key

    def request(self, discription, number_of_pictures, size):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "prompt": discription,
            "n": number_of_pictures,
            "size": size,
        }
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload,
            )
        except Exception as err:
            pass

        return json.loads(response.content)["data"][0]["url"]
