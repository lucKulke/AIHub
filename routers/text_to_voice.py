from fastapi import APIRouter


router = APIRouter(prefix="/text_to_voice", tags=["Text to voice"])


@router.post("/microsoft")
def microsoft_voices():
    pass
