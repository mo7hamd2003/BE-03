import os
from dotenv.main import load_dotenv
import jwt
from jwt import PyJWKClient
from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, field_validator
from supabase import Client
from database import get_supabase


load_dotenv()
router = APIRouter()
security = HTTPBearer(auto_error=False)

# Supabase signs tokens with ES256; public keys are fetched from JWKS and cached
JWKS_CLIENT = PyJWKClient(f"{os.getenv('SUPABASE_URL')}/auth/v1/.well-known/jwks.json")

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
    

def get_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Client = Depends(get_supabase),
):
    """Extract the JWT from the Authorization header and validate it against Supabase."""
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Access token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        response = db.auth.get_user(credentials.credentials)
        return response.user
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
