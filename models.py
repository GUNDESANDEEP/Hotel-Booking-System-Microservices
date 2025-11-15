# models.py
import sqlite3
from typing import List, Dict, Any

DB = "data.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def get_hotels() -> List[Dict[str, Any]]:
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id,name,location FROM hotels")
    rows = c.fetchall(); conn.close()
    return [{"id": r[0], "name": r[1], "location": r[2]} for r in rows]

def get_rooms(hotel_id: int):
    conn = get_conn(); c = conn.cursor()
    c.execute("SELECT id,room_type,price FROM rooms WHERE hotel_id=?", (hotel_id,))
    rows=c.fetchall(); conn.close()
    return [{"id":r[0],"room_type":r[1],"price":r[2]} for r in rows]

def create_booking(user_id:int, room_id:int, start:str, end:str):
    conn = get_conn(); c = conn.cursor()
    c.execute("INSERT INTO bookings (user_id,room_id,start_date,end_date) VALUES (?,?,?,?)",
              (user_id,room_id,start,end))
    conn.commit(); bid=c.lastrowid; conn.close()
    return bid

def get_bookings_by_user(user_id:int):
    conn=get_conn(); c=conn.cursor()
    c.execute("""SELECT b.id,b.room_id,b.start_date,b.end_date,h.name,r.room_type 
                 FROM bookings b 
                 JOIN rooms r ON b.room_id=r.id
                 JOIN hotels h ON r.hotel_id=h.id
                 WHERE b.user_id=?""",(user_id,))
    rows=c.fetchall(); conn.close()
    return [{"id":r[0],"room_id":r[1],"start":r[2],"end":r[3],"hotel":r[4],"room_type":r[5]} for r in rows]
