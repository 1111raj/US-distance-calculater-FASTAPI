# app.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Simple Calculator", version="1.0")

class AddPayload(BaseModel):
    x: float
    y: float

@app.get("/")
def root():
    return {"message": "Simple Calculator: use /add (GET or POST)"}

@app.get("/add")
def add_get(x: float = Query(...), y: float = Query(...)):
    """Example: /add?x=1&y=1  -> {"result": 2.0}"""
    return {"result": x + y}

@app.post("/add")
def add_post(payload: AddPayload):
    """POST JSON: {"x": 1, "y": 1} -> {"result": 2.0}"""
    return {"result": payload.x + payload.y}
