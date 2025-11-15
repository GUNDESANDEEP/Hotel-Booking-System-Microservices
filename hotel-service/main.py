# hotel-service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="hotel-service")

class Hotel(BaseModel):
    id: int
    name: str
    location: str
    price: float
    rating: float

class Room(BaseModel):
    id: int
    hotel_id: int
    room_type: str
    price: float

# In-memory sample data
_hotels: List[Dict] = [
    {"id": 1, "name": "Seaside Hotel", "location": "Goa", "price": 120.0, "rating": 4.5},
    {"id": 2, "name": "Mountain View Inn", "location": "Manali", "price": 90.0, "rating": 4.2}
]
_rooms: List[Dict] = [
    {"id": 1, "hotel_id": 1, "room_type": "Deluxe", "price": 120.0},
    {"id": 2, "hotel_id": 1, "room_type": "Standard", "price": 80.0},
    {"id": 3, "hotel_id": 2, "room_type": "Suite", "price": 150.0}
]

@app.get("/hotels", response_model=List[Hotel])
def list_hotels():
    return _hotels

@app.get("/hotels/{hotel_id}/rooms", response_model=List[Room])
def list_rooms(hotel_id: int):
    rooms = [r for r in _rooms if r["hotel_id"] == hotel_id]
    return rooms

@app.get("/health")
def health():
    return {"status": "ok"}
