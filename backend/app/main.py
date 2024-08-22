from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .routers import dashboard
import os

load_dotenv()  # Load environment variables

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",  # Local development
    "https://darc-frontend.vercel.app/",  # Vercel frontend domain
    os.getenv("NEXT_PUBLIC_BACKEND_URL")  # Render backend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the dashboard router
app.include_router(dashboard.routers)


@app.get("/")
def read_root():
    return {"message": "Welcome to the DARC API"}

