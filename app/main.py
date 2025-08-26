from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from pydantic import BaseModel
import os

from app.models import load_aircraft_data
from app.optimizer import load_route, estimate_fuel, optimize_routes

app = FastAPI(title="Airline Fuel Optimization API")

# Ensure data dir exists
os.makedirs("data", exist_ok=True)

# load once; you can reload if you change the CSV on disk
_aircraft_cache = load_aircraft_data("data/aircraft.csv")

class RouteFiles(BaseModel):
    files: list[str]

@app.get("/")
def home():
    return {
        "message": "Welcome to Airline Fuel Optimization API!",
        "endpoints": {
            "/aircraft": "List available aircraft (from data/aircraft.csv)",
            "/estimate/{aircraft_type}/{route_file}": "Estimate fuel for a given aircraft + route CSV",
            "/optimize/{aircraft_type} (POST)": "Compare multiple routes (JSON body: {\"files\":[..]})",
            "/upload-route/ (POST multipart)": "Upload a route CSV to data/"
        }
    }

@app.get("/aircraft")
def list_aircraft():
    # reload to pick any file changes
    global _aircraft_cache
    _aircraft_cache = load_aircraft_data("data/aircraft.csv")
    return {k: vars(v) for k, v in _aircraft_cache.items()}

@app.get("/estimate/{aircraft_type}/{route_file}")
def estimate_route(aircraft_type: str, route_file: str):
    # Validate aircraft
    if aircraft_type not in _aircraft_cache:
        raise HTTPException(status_code=404, detail=f"Aircraft {aircraft_type} not found")

    path = os.path.join("data", route_file)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Route file {route_file} not found")

    route = load_route(path)
    estimation = estimate_fuel(_aircraft_cache[aircraft_type], route)
    return {"aircraft": aircraft_type, "route_file": route_file, **estimation}

@app.post("/optimize/{aircraft_type}")
def optimize(aircraft_type: str, body: RouteFiles = Body(...)):
    # body.files is a list of CSV filenames (strings)
    result = optimize_routes(aircraft_type, body.files, aircraft_file="data/aircraft.csv")
    return result

@app.post("/upload-route/")
async def upload_route(file: UploadFile = File(...)):
    """
    Upload a route CSV to the server (saves to data/<filename>).
    Use Swagger to upload or curl:
    curl -F "file=@routes_option_b.csv" http://localhost:8000/upload-route/
    """
    dest = os.path.join("data", file.filename)
    # simple validation
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed")
    with open(dest, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return {"filename": file.filename, "status": "uploaded"}
