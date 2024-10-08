from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .routers import dashboard, collab, chat, auth, session
import os

app = FastAPI()

allowed_origins = [
    "https://darc.tecnivohub.com",
    "https://darc-frontend.netlify.app"
]

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.routers)
app.include_router(chat.routers)
app.include_router(auth.routers)
app.include_router(session.routers, prefix="/sessions")
app.include_router(collab.routers)

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
