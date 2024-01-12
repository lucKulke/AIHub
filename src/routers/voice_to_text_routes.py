from fastapi import APIRouter, UploadFile, File, HTTPException, Security, Form, Depends
from ..ai_services.voice_to_text_services import SpeechRecogniser
from ..utilitys import aws, converter

from typing import Annotated
import re, io, time, os, uuid, asyncio, base64, requests

from ..security.handler import get_current_active_user
from ..security.security_schemas import User
from ..schemas.voice_to_text_schemas import RunPodSchema


router = APIRouter(prefix="/voice_to_text", tags=["Voice to text"])

aws_bucket = os.getenv("AWS_BUCKET_NAME")

speech_recogniser = SpeechRecogniser(
    serverful_url=os.getenv("WHISPER_DOCKERIZED_URL"),
    runpod_api_key=os.getenv("RUNPOD_KEY"),
)


@router.post("/whisper/")
async def local_whisper_response(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["whisper"])
    ],
    audiofile: UploadFile = File(...),
    model: str = "small",
    only_text: bool = True,
    timeout: float = 86400.0,  # 24 hours
):
    audiofile_validation(audiofile)

    if audiofile.content_type == "audio/webm":
        audiofile = converter.audio_webm_to_mp3(audiofile)

    file_content = audiofile.file.read()
    audiofile.file.seek(0)

    s3_task = upload_to_s3(audiofile)
    whisper_task = speech_recogniser.request_severful_whisper(
        filename=audiofile.filename, content=file_content, model=model, timeout=timeout
    )

    whisper_result, s3_task_result = await asyncio.gather(
        whisper_task, s3_task
    )  # Wait for both tasks to complete

    response = whisper_result
    text = get_only_text(response)

    if only_text == True:
        response = text

    return {"whisper_result": response, "file_status": s3_task_result}


@router.post("/whisper/runpod_endpoint")
async def whisper_runpod_endpoint_response(
    current_user: Annotated[
        User, Security(get_current_active_user, scopes=["runpod_endpoint"])
    ],
    instructions: RunPodSchema = Depends(),
    timeout: float = 86400.0,
    only_text: bool = True,
    audiofile: UploadFile = File(...),
):
    audiofile_validation(audiofile)

    file_content = audiofile.file.read()
    audiofile.file.seek(0)
    base64_content = base64.b64encode(file_content).decode("utf-8")

    runpod_task = speech_recogniser.request_runpod_endpoint(
        audiofile_content=base64_content,
        timeout=timeout,
        instructions=instructions.__dict__,
    )
    s3_task = upload_to_s3(audiofile)

    runpod_result, s3_result = await asyncio.gather(runpod_task, s3_task)

    if only_text == True:
        text = ""
        for segment in runpod_result["output"]["segments"]:
            text += segment["text"]
        runpod_result = text.lstrip()

    return {"whisper_result": runpod_result, "file_status": s3_result}


def get_only_text(response: dict):
    text = ""
    for segment in response["predictions"]["segments"]:
        text += segment[4]
    return text.lstrip()


def audiofile_validation(audiofile: UploadFile):
    print(audiofile.content_type)
    if not audiofile.content_type in [
        "video/webm",
        "audio/webm",
        "audio/x-wav",
        "audio/wave",
        "audio/wav",
        "audio/mp3",
        "audio/ogg",
        "audio/mpeg",
    ]:
        raise HTTPException(
            status_code=400,
            detail=f"file: {audiofile.filename} is not an audiofile! possible formats: webm, wav-x, wav, mp3, ogg, mpeg",
        )


async def upload_to_s3(audiofile: UploadFile):
    file_like_obj = audiofile.file

    filename = re.match(r"(.+?)\.\w+", audiofile.filename).group(
        1
    )  # get filename without extension

    file_extension = re.search(r"/(\w+)", audiofile.content_type).group(1)
    key = f"{filename}_{uuid.uuid4()}.{file_extension}"

    response = await aws.upload_file_content_directly_to_s3(
        file_like_obj, aws_bucket, key, audiofile.content_type
    )
    return response
