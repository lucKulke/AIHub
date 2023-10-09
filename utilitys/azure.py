import requests


def get_access_token(subscription_key):
    fetch_token_url = (
        "https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    )
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(fetch_token_url, headers=headers)
    return str(response.text)


def text_to_voice(text, access_token):
    headers = {
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "Content-Type": "application/ssml+xml",
        "Host": "westeurope.tts.speech.microsoft.com",
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "AIHub",
    }

    xml_body = f"""
    <speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Male'
        name='en-US-ChristopherNeural'>
            {text}
    </voice></speak>
    """

    # Define the URL for the POST request
    url = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"

    # Send the POST request
    return requests.post(url, headers=headers, data=xml_body)
