from fastapi import APIRouter


router = APIRouter(prefix="/voice_to_text", tags=["Voice to text"])


@router.post("/whisper")
def whisper_response():
    pass
