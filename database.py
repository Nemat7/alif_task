import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple

DATABASE_NAME = "booking_office.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cabinet_number INTEGER NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        user_name TEXT NOT NULL,
        user_email TEXT NOT NULL,
        user_phone TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def check_availability(cabinet_number: int, start_time:datetime, end_time:datetime)->Optional[Tuple]:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_name, end_time 
    FROM bookings 
    WHERE cabinet_number = ? 
    AND ((start_time BETWEEN ? AND ?) 
    OR (end_time BETWEEN ? AND ?) 
    OR (start_time <= ? AND end_time >= ?))
    """, (cabinet_number, start_time, end_time, start_time, end_time, start_time, end_time))

    result = cursor.fetchone()
    conn.close()

    return result


def add_booking(cabinet_number: int, start_time: datetime, end_time: datetime, user_name: str, user_email: str, user_phone: str)-> bool:
    if check_availability(cabinet_number, start_time, end_time):
        return False
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO bookings (cabinet_number, start_time, end_time, user_name, user_email, user_phone)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (cabinet_number, start_time, end_time, user_name, user_email, user_phone))

    conn.commit()
    conn.close()
    return True