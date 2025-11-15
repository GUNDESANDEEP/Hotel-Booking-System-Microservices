# booking-service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="booking-service")

class BookingReq(BaseModel):
    user_id: int
    hotel_id: int
    room_id: int
    start_date: str
    end_date: str

# In-memory store of bookings
_bookings: List[Dict] = []
_next_id = 1

@app.post("/bookings")
def create_booking(b: BookingReq):
    global _next_id
    rec = {"id": _next_id, **b.dict()}
    _bookings.append(rec)
    _next_id += 1
    return rec

@app.get("/bookings", response_model=List[Dict])
def list_bookings():
    return _bookings

@app.get("/health")
def health():
    return {"status": "ok"}
