from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .routers import dashboard, collab, chat, auth
import os

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.routers)
app.include_router(collab.routers)
app.include_router(chat.routers)
app.include_router(auth.routers)

@app.get("/")
def read_root():
    return {"message": "Welcome to the DARC API"}

# WebSocket endpoint for collaborative editing
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await collab.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            await collab.broadcast(session_id, data)
    except WebSocketDisconnect:
        await collab.disconnect(websocket, session_id)
