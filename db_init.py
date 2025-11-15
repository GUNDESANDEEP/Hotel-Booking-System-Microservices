# db_init.py
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT UNIQUE,
  password_hash TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS hotels (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  location TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS rooms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  hotel_id INTEGER,
  room_type TEXT,
  price REAL,
  FOREIGN KEY(hotel_id) REFERENCES hotels(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  room_id INTEGER,
  start_date TEXT,
  end_date TEXT,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(room_id) REFERENCES rooms(id)
)
''')

# Seed sample hotel, room, and user if not present
c.execute("INSERT OR IGNORE INTO hotels (id, name, location) VALUES (1, 'Seaside Hotel', 'Goa')")
c.execute("INSERT OR IGNORE INTO rooms (id, hotel_id, room_type, price) VALUES (1, 1, 'Deluxe', 100.0)")
c.execute("INSERT OR IGNORE INTO users (id, name, email, password_hash) VALUES (1, 'Demo User', 'demo@example.com', 'demo')")

conn.commit()
conn.close()
print("DB initialized.")
