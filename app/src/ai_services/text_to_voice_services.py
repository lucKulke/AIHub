import requests
import json
import os


class AzureVoice:
    def __init__(self, subscription_key, azure_token_url, ctms_url):
        self.speakers = self.list_of_available_speakers()
        self.subscription_key = subscription_key
        self.azure_token_url = azure_token_url
        self.ctms_url = ctms_url

    def get_access_token(self):
        body = {
            "subscription_key": self.subscription_key,
            "server_url": self.azure_token_url,
        }
        response = requests.post(self.ctms_url, json=body)
        return response.json().get("access_token")

    def generate_voice(self, text, language):
        access_token = self.get_access_token()
        speaker = self.speakers[language]

        headers = {
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "Content-Type": "application/ssml+xml",
            "Host": "westeurope.tts.speech.microsoft.com",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "AIHub",
        }

        xml_body = f"""
        <speak version='1.0' xml:lang='{speaker['language']}'><voice xml:lang='{speaker['language']}' xml:gender='{speaker['gender']}'
            name='{speaker['name']}'>
                {text}
        </voice></speak>
        """

        url = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"

        return requests.post(url, headers=headers, data=xml_body.encode("utf-8"))

    def list_of_azure_voices(self):
        access_token = self.get_access_token()

        headers = {
            "Host": "westeurope.tts.speech.microsoft.com",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "AIHub",
        }

        url = (
            "https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list"
        )
        response = requests.get(url, headers=headers)

        return response.content

    def list_of_available_speakers(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        languages_json_path = os.path.join(script_directory, "languages.json")
        try:
            with open(languages_json_path, "r") as json_file:
                return json.load(json_file)
        except Exception as e:
            raise e

    def list_of_available_languages(self):
        return list(self.speakers.keys())

    def is_language_available(self, language):
        return language in self.list_of_available_languages()
