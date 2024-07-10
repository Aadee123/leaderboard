from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect('leaderboard.db', check_same_thread=False)
cursor = conn.cursor()

# Create a table for the leaderboard if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER NOT NULL
)
''')
conn.commit()

# Define the request body schema
class PlayerScore(BaseModel):
    name: str
    score: int

# Endpoint to add a new score
@app.post("/add_score/")
async def add_score(player_score: PlayerScore):
    cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (player_score.name, player_score.score))
    conn.commit()
    return {"message": "Score added successfully"}

# Endpoint to get the leaderboard
@app.get("/leaderboard/")
async def get_leaderboard():
    cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC")
    leaderboard = cursor.fetchall()
    return {"leaderboard": leaderboard}

