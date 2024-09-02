from fastapi import APIRouter, WebSocket
from typing import Dict, List

routers = APIRouter()

chat_connections: Dict[str, List[WebSocket]] = {}

async def connect(websocket: WebSocket, session_id: str):
    await websocket.accept()
    if session_id not in chat_connections:
        chat_connections[session_id] = []
    chat_connections[session_id].append(websocket)

async def disconnect(websocket: WebSocket, session_id: str):
    chat_connections[session_id].remove(websocket)
    if not chat_connections[session_id]:
        del chat_connections[session_id]

async def broadcast_message(session_id: str, message: str):
    for connection in chat_connections[session_id]:
        await connection.send_text(message)
