from fastapi import Depends, APIRouter

router = APIRouter()

@router.get("/public/info")
async def public_info():
    return { "status_code": 200, "message": "Welcome Stranger, this info is public"}