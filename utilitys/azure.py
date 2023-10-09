import requests


def get_access_token(subscription_key):
    fetch_token_url = (
        "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    )
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(fetch_token_url, headers=headers)
    return str(response.text)
