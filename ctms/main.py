from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from threading import Lock
from datetime import datetime, timedelta
import requests

ctms = FastAPI()
lock = Lock()

AZURE_ACCESS_TOKEN = None
AZURE_TOKEN_EXPIRATION_TIME = None


class AzureCredentials(BaseModel):
    subscription_key: str
    server_url: str


class TokenData(BaseModel):
    access_token: str


@ctms.post("/get_azure_token", response_model=TokenData)
def get_token(request: AzureCredentials):
    global AZURE_ACCESS_TOKEN, AZURE_TOKEN_EXPIRATION_TIME

    with lock:
        # Check if the token is still valid for a reasonable duration
        if (
            AZURE_TOKEN_EXPIRATION_TIME
            and AZURE_TOKEN_EXPIRATION_TIME > datetime.utcnow()
        ):
            return {
                "access_token": AZURE_ACCESS_TOKEN,
            }

        # Fetch a new token from FastAPI server
        new_token = fetch_new_token(request.subscription_key, request.server_url)
        AZURE_ACCESS_TOKEN = new_token
        AZURE_TOKEN_EXPIRATION_TIME = datetime.utcnow() + timedelta(
            minutes=8
        )  # Azure tokens last a maximum of 10 minutes

    return {"access_token": AZURE_ACCESS_TOKEN}


def fetch_new_token(subscription_key, server_url):
    print("fetching new token...", flush=True)
    try:
        fetch_token_url = server_url
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        response = requests.post(fetch_token_url, headers=headers)

        if response.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        if response.status_code == 403:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
    except requests.exceptions.RequestException as errex:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"The requested server url: {server_url} cannot be reached",
        )

    new_token = str(response.text)
    return new_token


if __name__ == "__main__":
    ctms.run(port=8003)
