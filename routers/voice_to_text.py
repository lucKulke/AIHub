from fastapi import APIRouter, Response, Form, UploadFile, File, HTTPException
from schemas.voice_to_text import WhisperSchema
from ai_services.voice_to_text import Whisper
import shutil
import os
from utilitys import aws
import boto3
import uuid
import tempfile
from datetime import datetime
import asyncio
import requests
import httpx
import typing
import re
import time


router = APIRouter(prefix="/voice_to_text", tags=["Voice to text"])

aws_bucket = os.getenv("AWS_BUCKET_NAME")

whisper = Whisper("http://localhost:8080")


@router.post("/whisper")
async def whisper_response(
    audiofile: UploadFile = File(...), model: str = Form(...), only_text: bool = True
):
    if not audiofile.content_type in [
        "audio/wave",
        "audio/wav",
        "audio/mp3",
        "audio/ogg",
        "audio/mpeg",
    ]:
        raise HTTPException(
            status_code=400,
            detail=f"file: {audiofile.filename} is not an audiofile! possible formats: wav, mp3, ogg, mpeg",
        )

    s3_task = upload_to_s3(audiofile)
    whisper_task = send_to_whisper(audiofile, model)

    whisper_result, s3_task_result = await asyncio.gather(
        whisper_task, s3_task
    )  # Wait for both tasks to complete

    response = whisper_result
    if only_text == True:
        response = response["predictions"]["segments"][0][4]

    return {"whisper_result": response, "file_status": s3_task_result}


async def upload_to_s3(audiofile: UploadFile):
    file_like_obj = audiofile.file

    filename = re.match(r"(.+?)\.\w+", audiofile.filename).group(
        1
    )  # get filename without extension

    file_extension = re.search(r"/(\w+)", audiofile.content_type).group(1)

    key = f"{filename}_{uuid.uuid4()}.{file_extension}"

    s3_upload_start = time.time()
    print(f"Uploading to s3...", flush=True)
    response = await aws.upload_file_content_directly_to_s3(
        file_like_obj, aws_bucket, key, audiofile.content_type
    )
    s3_upload_end = time.time()
    print(
        f"Upload to s3 finised. Time needed: {s3_upload_end - s3_upload_start}",
        flush=True,
    )
    return response


async def send_to_whisper(file: UploadFile, model: str):
    content = file.file.read()  # The file pointer is after read() at the end
    file.file.seek(0)  # Move the file pointer to the beginning of the file

    whisper_upload_start = time.time()
    print(f"Sending file to whisper for transcription...", flush=True)
    response = await whisper.request_with_upload_file_directly(
        file.filename, content, model
    )
    whisper_upload_end = time.time()
    print(
        f"Response from whisper received. Time needed: {whisper_upload_end - whisper_upload_start}",
        flush=True,
    )

    return response
