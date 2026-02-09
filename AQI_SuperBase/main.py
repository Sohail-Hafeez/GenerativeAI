from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database URL from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Use PostgreSQL (Production)
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2.pool import SimpleConnectionPool
    
    # Create connection pool for better performance
    pool = SimpleConnectionPool(1, 10, DATABASE_URL)
    
    def get_db_connection():
        return pool.getconn()
    
    def return_db_connection(conn):
        pool.putconn(conn)
    
    def init_db():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id SERIAL PRIMARY KEY,
                data JSONB NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        return_db_connection(conn)
else:
    # Use SQLite (Local development)
    import sqlite3
    DB_NAME = "esp32_data.db"
    
    def get_db_connection():
        return sqlite3.connect(DB_NAME)
    
    def return_db_connection(conn):
        conn.close()
    
    def init_db():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return_db_connection(conn)

# Initialize database on startup
init_db()

# Pydantic model for ESP32 data
class SensorData(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    # Add more sensor fields as needed

@app.post("/StoreData")
async def store_data(data: SensorData):
    try:
        conn = get_db_connection()
        data_json = json.dumps(data.dict())
        
        if DATABASE_URL:
            # PostgreSQL
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sensor_data (data) VALUES (%s) RETURNING id",
                (data_json,)
            )
            row_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
        else:
            # SQLite
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sensor_data (data) VALUES (?)",
                (data_json,)
            )
            row_id = cursor.lastrowid
            conn.commit()
        
        return_db_connection(conn)
        
        return {
            "status": "success",
            "message": "Data stored successfully",
            "id": row_id
        }
    except Exception as e:
        if 'conn' in locals():
            return_db_connection(conn)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getData")
async def get_data():
    try:
        conn = get_db_connection()
        
        if DATABASE_URL:
            # PostgreSQL
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT id, data, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            cursor.close()
        else:
            # SQLite
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, data, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
        
        return_db_connection(conn)
        
        if row is None:
            raise HTTPException(status_code=404, detail="No data found")
        
        if DATABASE_URL:
            # PostgreSQL returns dict
            return {
                "id": row['id'],
                "data": row['data'],
                "timestamp": str(row['timestamp'])
            }
        else:
            # SQLite returns tuple
            data_dict = json.loads(row[1])
            return {
                "id": row[0],
                "data": data_dict,
                "timestamp": row[2]
            }
    except HTTPException:
        raise
    except Exception as e:
        if 'conn' in locals():
            return_db_connection(conn)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "ESP32 Data API is running",
        "database": "PostgreSQL (Supabase)" if DATABASE_URL else "SQLite (Local)"
    }