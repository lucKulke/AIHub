from fastapi import APIRouter, Response, Form, UploadFile, File
from schemas.voice_to_text import WhisperSchema
import shutil
import os
from utilitys import aws
import boto3
import uuid
import tempfile

router = APIRouter(prefix="/voice_to_text", tags=["Voice to text"])

aws_bucket = os.getenv("AWS_BUCKET_NAME")
os.getenv("AWS_REGION")


@router.post("/whisper")
def whisper_response(audio_file: UploadFile = File(...), model: str = Form(...)):
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

                aws.upload_file_to_s3(temp_file_path, aws_bucket, filename)

        # Optionally, you can return the path of the saved file
        return Response(
            content=f"message : Audio file uploaded and saved to directory | filename: {filename}"
        )
    except Exception as e:
        return Response(content=f"error: {str(e)}", status_code=500)
