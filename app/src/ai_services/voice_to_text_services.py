import requests
from typing import BinaryIO
from fastapi import HTTPException, status, UploadFile
from datetime import datetime
import httpx, base64


class SpeechRecogniser:
    def __init__(self, serverful_url: str = "", runpod_api_key: str = ""):
        self.serverful_url = serverful_url
        self.runpod_api_key = runpod_api_key

    async def request_severful_whisper(
        self, filename: str, content: BinaryIO, model: str, timeout: float
    ):
        url = f"{self.server_url}/invocations/upload_file/?model_size={model}"

        files = {"audiofile": (filename, content, "audio/wav")}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    files=files,
                    timeout=timeout,
                )
                response.raise_for_status()
                json_response = response.json()
        except httpx.ReadTimeout as timeout_err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="TimeoutError"
            )
        except httpx.HTTPError as http_err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to connect to Whisper",
            )

        return json_response

    async def request_runpod_endpoint(
        self, audiofile_content: str, timeout: float, instructions: dict
    ):
        url = "https://api.runpod.ai/v2/faster-whisper/runsync"
        instructions["audio_base64"] = audiofile_content
        enable_vad = instructions.pop("enable_vad")
        payload = {
            "enable_vad": enable_vad,
            "input": instructions,
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.runpod_api_key,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=timeout,
                )

                response.raise_for_status()
                json_response = response.json()
        except httpx.ReadTimeout as timeout_err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="TimeoutError"
            )
        except httpx.HTTPError as http_err:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )

        return json_response
