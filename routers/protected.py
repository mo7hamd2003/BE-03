from fastapi import Depends, APIRouter
from .auth import get_current_user

router = APIRouter()

@router.get("/protect/profile")
def protected_profile(payload: dict = Depends(get_current_user)):
    return {"status_code": 200, "user_id": payload["sub"]}

    