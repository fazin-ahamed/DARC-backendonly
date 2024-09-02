from fastapi import APIRouter, WebSocket
from typing import List, Dict

router = APIRouter()

# Store sessions and connected users
active_connections: Dict[str, List[WebSocket]] = {}

async def connect(websocket: WebSocket, session_id: str):
    await websocket.accept()
    if session_id not in active_connections:
        active_connections[session_id] = []
    active_connections[session_id].append(websocket)

async def disconnect(websocket: WebSocket, session_id: str):
    active_connections[session_id].remove(websocket)
    if not active_connections[session_id]:
        del active_connections[session_id]

async def broadcast(session_id: str, message: str):
    for connection in active_connections[session_id]:
        await connection.send_text(message)
