from fastapi import FastAPI
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from routers import auth, health, protected, pub

# Stage-0: Load .env variables
load_dotenv()

# Stage-0: Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Stage-0: Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Stage-0: Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Stage-0: Try to connect
try:
    with engine.connect() as connection:
        print("Server running and connected to Supabase")
except Exception as e:
    print(f"Failed to connect: {e}")

app = FastAPI()
app.include_router(auth.router)
app.include_router(pub.router)
app.include_router(protected.router)
