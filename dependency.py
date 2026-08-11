import os
from dotenv.main import load_dotenv
from jwt import PyJWKClient
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from database import get_supabase

load_dotenv()

security = HTTPBearer(auto_error=False)

# Supabase signs tokens with ES256; public keys are fetched from JWKS and cached
JWKS_CLIENT = PyJWKClient(f"{os.getenv('SUPABASE_URL')}/auth/v1/.well-known/jwks.json")


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
