from fastapi import APIRouter, Response, Form, UploadFile, File
from schemas.voice_to_text import WhisperSchema
from ai_services.voice_to_text import Whisper
import shutil
import os
from utilitys import aws
import boto3
import uuid
import tempfile
import time

router = APIRouter(prefix="/voice_to_text", tags=["Voice to text"])

aws_bucket = os.getenv("AWS_BUCKET_NAME")
os.getenv("AWS_REGION")


@router.post("/whisper")
def whisper_response(
    audio_file: UploadFile = File(...), model: str = Form(...), only_text: bool = True
):
    upload_directory = "./temp_audio"
    try:
        # Ensure the specified directory exists; create it if not

        filename = "recording_" + str(uuid.uuid4()) + ".wav"
        # Combine the directory path with the uploaded audio file's name

        # Save the uploaded audio file to the specified directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate a unique filename for the uploaded audio file
            temp_file_path = f"{temp_dir}/{filename}"

            # Save the uploaded audio file to the temporary directory
            with open(temp_file_path, "wb") as f:
                f.write(audio_file.file.read())

                success = aws.upload_file_to_s3(temp_file_path, aws_bucket, filename)
                if success:
                    presigned_url = aws.create_presigned_url_expanded(
                        "get_object",
                        {"Bucket": aws_bucket, "Key": filename},
                        http_method="GET",
                    )

                    print(presigned_url, flush=True)
                    response = Whisper("http://localhost:8080/invocations").request(
                        presigned_url, model
                    )

        # Optionally, you can return the path of the saved file
        if only_text:
            return response["predictions"]["segments"][0][4]
        else:
            return response
    except Exception as e:
        print(f"error: {str(e)}")
        return Response(content=f"error: {str(e)}", status_code=500)
