from fastapi import APIRouter, HTTPException
import uuid

routers = APIRouter()

# Store sessions in-memory for demonstration purposes
sessions = {}

@routers.post("/create-session")
async def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = []  # Initialize session data
    return {"session_id": session_id}

@routers.post("/join-session")
async def join_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id}
