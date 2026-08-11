from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_endpoint():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/auth"]}