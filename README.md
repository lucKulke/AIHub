# AIHub API

AIHub is an API that provides access to various AI services, allowing users to leverage powerful artificial intelligence capabilities in their applications. This API supports a range of functionalities, including but not limited to language processing, image generation, audio processing, and more. All the traffic data is stored in a postgress database so make sure to setup a database before starting the AIHub.

### Getting Started

To use the AIHub API, follow these steps:

**Installation:**

- Clone the repository: git clone https://github.com/lucKulke/AIHub.git
- Install dependencies: pip install -r requirements.txt

**Configuration:**

- Set up your environment variables with the required API keys, endpoints and more. Here are the environment variables:

```zsh
DB_PORT = "Database server port"
DB_TYPE = "PostgreSQL"
DB_HOST = "Database host"
DB_NAME = "Database name"
DB_USERNAME = "Database username"
DB_PASSWORD = "Database password"

OPEN_AI_KEY = "OpenAi api key (for chat-gpt and dalle)"
AWS_ACCESS_KEY_ID = "Amazon IAM user access-key"
AWS_SECRET_ACCESS_KEY = "Amazon IAM user secret-access-key"
AWS_BUCKET_NAME = "Amazon s3 bucket name (for file storage)"
AWS_BUCKET_REGION = "Amazon s3 bucket region"
AZURE_VOICE_SUBSCRIPTION_KEY = "Azure voice subscription key for voice generation"

```

**Run the API:**

- Start the API server: `uvicorn main:app --reload --port 8001`
- The API will be available at http://localhost:8000 by default.

**Usage**:

After starting the AIHub server visit the `/docs` route to see the required request formats and testing the services.
