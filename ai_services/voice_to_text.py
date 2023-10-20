import requests


class Whisper:
    def __init__(self, server_url):
        self.server_url = server_url

    def request(self, presigned_url, model):
        payload = {"model": model, "input": presigned_url}
        try:
            response = requests.post(self.server_url, json=payload)
        except Exception as err:
            response = f"error in whisper service: {err}"
        return response.json()
