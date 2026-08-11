from fastapi import Depends, APIRouter
from .auth import get_user

router = APIRouter()

@router.get("/protect/profile")
def protected_profile(user=Depends(get_user)):
    return {"status_code": 200, "user": user}

    