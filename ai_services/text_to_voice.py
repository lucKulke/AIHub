import requests
from utilitys import azure
import json


class AzureVoice:
    def __init__(self):
        self.speakers = self.list_of_available_speakers()

    def set_access_token(self, token):
        self.access_token = token

    def get_access_token(subscription_key):
        fetch_token_url = (
            "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        )
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        response = requests.post(fetch_token_url, headers=headers)
        return str(response.text)

    def generate_voice(self, text, language):
        speaker = self.speakers[language]

        headers = {
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "Content-Type": "application/ssml+xml",
            "Host": "westeurope.tts.speech.microsoft.com",
            "Authorization": f"Bearer {self.access_token}",
            "User-Agent": "AIHub",
        }

        xml_body = f"""
        <speak version='1.0' xml:lang='{speaker['language']}'><voice xml:lang='{speaker['language']}' xml:gender='{speaker['gender']}'
            name='{speaker['name']}'>
                {text}
        </voice></speak>
        """

        # Define the URL for the POST request
        url = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"

        # Send the POST request
        return requests.post(url, headers=headers, data=xml_body.encode("utf-8"))

    def list_of_azure_voices(self, subkey):
        token = azure.get_access_token(subkey)

        headers = {
            "Host": "westeurope.tts.speech.microsoft.com",
            "Authorization": f"Bearer {token}",
            "User-Agent": "AIHub",
        }

        url = (
            "https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list"
        )
        response = requests.get(url, headers=headers)

        return response.content

    def list_of_available_speakers(self):
        try:
            with open("languages.json", "r") as json_file:
                return json.load(json_file)
        except Exception as e:
            raise e

    def list_of_available_languages(self):
        return list(self.speakers.keys())

    def is_language_available(self, language):
        return language in self.list_of_available_languages()
