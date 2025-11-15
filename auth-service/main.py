# auth-service/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="auth-service")

# Very simple in-memory user store for prototype
_USERS = {
    1: {"id": 1, "name": "Demo User", "email": "demo@example.com"}
}

class LoginRequest(BaseModel):
    email: str

@app.post("/login")
def login(req: LoginRequest) -> Dict:
    # Prototype: accept any email, return the demo user and a fake token
    user = _USERS[1]
    token = "fake-token"
    return {"token": token, "user": user}

@app.get("/health")
def health():
    return {"status": "ok"}
