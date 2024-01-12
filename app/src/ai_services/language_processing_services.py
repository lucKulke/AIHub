import httpx


class ChatGPT:
    def __init__(self, key):
        self.set_api_key(key)

    def set_api_key(self, key):
        self.key = key

    async def request(self, instance, model, system_message, conversation, token):
        conversation.insert(0, {"role": "system", "content": system_message})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}",
        }

        payload = {"model": model, "messages": conversation, "max_tokens": token}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30.00,
                )
                response.raise_for_status()  # Raise an exception if the response indicates an error

            json_response = response.json()
            message = json_response["choices"][0]["message"]
            response_data = {instance: message}

        except httpx.ReadTimeout as timeout_err:
            response_data = {
                instance: {"role": "error", "content": "httpx ReadTimeout error"}
            }

        except httpx.HTTPError as http_err:
            response_data = {instance: {"role": "error", "content": f"httpx error"}}

        except Exception as err:
            response_data = {instance: f"An error occurred: {err}"}

        return response_data
