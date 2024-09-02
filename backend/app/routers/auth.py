from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

routers = APIRouter()

class User(BaseModel):
    username: str
    role: str

# Placeholder for user authentication
users = {"admin": "admin123", "developer": "dev123"}

# Sample role-based permissions
roles_permissions = {
    "admin": ["create", "edit", "delete", "view"],
    "developer": ["edit", "view"]
}

@router.post("/login")
def login(user: User):
    if user.username in users and users[user.username] == user.password:
        return {"status": "success", "message": f"Welcome, {user.username}!"}
    raise HTTPException(status_code=401, detail="Unauthorized")
