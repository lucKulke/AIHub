from fastapi import APIRouter


router = APIRouter(prefix="/ai_service", tags=["AI Services"])


@router.get("/")
def test():
    return {"Hello World"}
