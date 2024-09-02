from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

routers = APIRouter()

# Store WebSocket connections by session_id
connections: Dict[str, list] = {}

@routers.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    if session_id not in connections:
        connections[session_id] = []

    await websocket.accept()
    connections[session_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections[session_id]:
                if connection != websocket:
                    await connection.send_text(data)
    except WebSocketDisconnect:
        connections[session_id].remove(websocket)
        if not connections[session_id]:
            del connections[session_id]
