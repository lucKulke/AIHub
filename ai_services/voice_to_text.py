import requests
from typing import BinaryIO
from fastapi import HTTPException, status
from datetime import datetime
import httpx


class Whisper:
    def __init__(self, server_url):
        self.server_url = server_url

    async def request_with_upload_file_directly(
        self, filename: str, content: BinaryIO, model: str, timeout: float
    ):
        whisper_api_url = (
            f"{self.server_url}/invocations/upload_file/?model_size={model}"
        )

        files = {"audiofile": (filename, content, "audio/wav")}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    whisper_api_url,
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
