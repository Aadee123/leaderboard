from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import uuid

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect('leaderboard.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table for the leaderboard if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS leaderboard (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER NOT NULL
)
''')
conn.commit()

# Define the request body schema for adding a new score
class PlayerScore(BaseModel):
    name: str
    score: int

# Define the request body schema for updating a score
class UpdateScore(BaseModel):
    id: str
    score: int

# Endpoint to add a new score
@app.post("/add_score/")
async def add_score(player_score: PlayerScore):
    user_id = str(uuid.uuid4())  # Generate a unique user ID
    cursor.execute("INSERT INTO leaderboard (id, name, score) VALUES (?, ?, ?)", (user_id, player_score.name, player_score.score))
    conn.commit()
    return {"message": "Score added successfully", "user_id": user_id}

# Endpoint to get the leaderboard
@app.get("/leaderboard/")
async def get_leaderboard():
    cursor.execute("SELECT id, name, score FROM leaderboard ORDER BY score DESC")
    leaderboard = cursor.fetchall()
    return {"leaderboard": leaderboard}

# Endpoint to update a score
@app.put("/update_score/")
async def update_score(update_score: UpdateScore):
    cursor.execute("SELECT * FROM leaderboard WHERE id = ?", (update_score.id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    cursor.execute("UPDATE leaderboard SET score = ? WHERE id = ?", (update_score.score, update_score.id))
    conn.commit()
    return {"message": "Score updated successfully"}


