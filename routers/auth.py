import os
from dotenv.main import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator
from supabase import Client
from database import get_supabase
from dependency import get_user


load_dotenv()
router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_not_empty(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("email is required")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v):
        if v is None:
            return v
        if not v.strip():
            raise ValueError("password is required")
        return v.strip()
    

@router.post("/auth/signup")
def sign_up(user: UserCreate, db: Client = Depends(get_supabase)):
    try:
        response = db.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return {"status_code": 201, "message": "User created successfully", "data": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/login")
def login(credentials: UserCreate, db: Client = Depends(get_supabase)):
    try:
        response = db.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password,
        })
        return {
            "status_code": 200,
            "message": "Login successful",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/auth/logout")
def logout(user=Depends(get_user), db: Client = Depends(get_supabase)):
    try:
        db.auth.sign_out()
        return {"status_code": 204, "message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
