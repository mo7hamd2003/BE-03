import os
from dotenv.main import load_dotenv
import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, field_validator
from supabase import Client
from database import get_supabase


load_dotenv()

key=os.getenv("SUPABASE_JWT_SECRET")

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
    


def get_current_user(authorization: str = Header(...)):
    try:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise ValueError("invalid scheme")
        payload = jwt.decode(
            token,
            key,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


@router.post("/signup")
def sign_up(user: UserCreate, db: Client = Depends(get_supabase)):
    try:
        response = db.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return {"status_code": 201, "message": "User created successfully", "data": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
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
