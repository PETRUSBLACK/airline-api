# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from typing import List
from .optimizer import load_aircraft_data, load_route, estimate_fuel, optimize_routes
from .agent import ask_agent
import os

app = FastAPI(
    title="Airline Fuel Optimization API",
    description="Estimate and optimize fuel usage for aircraft routes. Includes an AI assistant endpoint.",
    version="1.0.0",
)

# Ensure data dir exists
os.makedirs("data", exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to Airline Fuel Optimization API!",
        "endpoints": {
            "/aircraft": "List available aircraft (from data/aircraft.csv)",
            "/estimate/{aircraft_type}/{route_file}": "Estimate fuel for an aircraft on one route CSV",
            "/optimize/{aircraft_type} (POST)": "Compare multiple route CSVs (JSON body: list of filenames)",
            "/ask-agent?question=...": "Ask the AI assistant a question about routes/fuel",
            "/upload-route/ (POST multipart)": "Upload a route CSV to data/"
        }
    }


@app.get("/aircraft")
def list_aircraft():
    """
    Returns all aircraft loaded from data/aircraft.csv
    """
    try:
        aircraft_data = load_aircraft_data("data/aircraft.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="data/aircraft.csv not found")
    # Convert Aircraft objects to dicts for JSON serialization
    return {k: vars(v) for k, v in aircraft_data.items()}


@app.get("/estimate/{aircraft_type}/{route_file}")
def estimate(aircraft_type: str, route_file: str):
    """
    Estimate total fuel for a single route file.
    Example: GET /estimate/A320/routes.csv
    """
    try:
        aircraft_data = load_aircraft_data("data/aircraft.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="data/aircraft.csv not found")

    if aircraft_type not in aircraft_data:
        raise HTTPException(status_code=404, detail=f"Aircraft {aircraft_type} not found")

    path = os.path.join("data", route_file)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Route file {route_file} not found")

    route = load_route(path)
    fuel = estimate_fuel(aircraft_data[aircraft_type], route)
    return {"aircraft": aircraft_type, "route_file": route_file, "fuel_estimate_kg": fuel}


@app.post("/optimize/{aircraft_type}")
def optimize(aircraft_type: str, route_files: List[str] = Body(...)):
    """
    Compare several route CSV files for the given aircraft.
    Body example (raw JSON):
      ["routes.csv", "routes_option_b.csv", "routes_option_c.csv"]
    """
    try:
        result = optimize_routes(aircraft_type, route_files, aircraft_file="data/aircraft.csv")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/ask-agent")
def ask_ai(question: str):
    """
    Ask the AI assistant a freeform question (returns a text answer).
    Example: /ask-agent?question=Which%20route%20saves%20the%20most%20fuel%3F
    """
    try:
        answer = ask_agent(question)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-route/")
async def upload_route(file: UploadFile = File(...)):
    """
    Upload a route CSV (saves to data/<filename>).
    Use Swagger or curl:
      curl -F "file=@routes_option_b.csv" http://localhost:8000/upload-route/
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed")
    dest = os.path.join("data", file.filename)
    with open(dest, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return {"filename": file.filename, "status": "uploaded"}
