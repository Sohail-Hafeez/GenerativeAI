from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sqlite3
from datetime import datetime
import json

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_NAME = "esp32_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Pydantic model for incoming ESP32 data
class SensorData(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    # Add more fields as needed based on your ESP32 sensors

@app.post("/StoreData")
async def store_data(data: SensorData):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Convert data to JSON string
        data_json = json.dumps(data.dict())
        
        cursor.execute(
            "INSERT INTO sensor_data (data) VALUES (?)",
            (data_json,)
        )
        conn.commit()
        row_id = cursor.lastrowid
        conn.close()
        
        return {
            "status": "success",
            "message": "Data stored successfully",
            "id": row_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getData")
async def get_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Get the latest row
        cursor.execute(
            "SELECT id, data, timestamp FROM sensor_data ORDER BY id DESC LIMIT 1"
        )
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            raise HTTPException(status_code=404, detail="No data found")
        
        # Parse the JSON data
        data_dict = json.loads(row[1])
        
        return {
            "id": row[0],
            "data": data_dict,
            "timestamp": row[2]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "ESP32 Data API is running"}

# Run with: uvicorn main:app --reload