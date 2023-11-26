import requests


from datetime import datetime
import httpx


class Whisper:
    def __init__(self, server_url):
        self.server_url = server_url

    async def request_with_upload_file_directly(self, filename, content, model):
        whisper_api_url = (
            f"{self.server_url}/invocations/upload_file/?model_size={model}"
        )

        files = {"audiofile": (filename, content, "audio/wav")}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    whisper_api_url,
                    files=files,
                    timeout=100.00,
                )
                response.raise_for_status()
                json_response = response.json()
        except httpx.ReadTimeout as timeout_err:
            json_response = {{"ReadTimeoutError": f"Timeout error: {timeout_err}"}}
        except httpx.HTTPError as http_err:
            json_response = {"HTTPError": f"HTTP error: {http_err.response.content}"}

        return json_response
