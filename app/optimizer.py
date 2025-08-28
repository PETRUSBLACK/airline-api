import pandas as pd
from .models import Aircraft, RouteSegment

def load_aircraft_data(file_path="aircraft.csv"):
    df = pd.read_csv(file_path)
    data = {}
    for _, row in df.iterrows():
        data[row["aircraft_type"]] = Aircraft(
            row["aircraft_type"], row["cruise_speed"], row["fuel_burn_per_hour"]
        )
    return data

def load_route(file_path):
    df = pd.read_csv(file_path)
    return [
        RouteSegment(r["waypoint"], r["distance_km"], r["wind"], r["turbulence"])
        for _, r in df.iterrows()
    ]

def estimate_fuel(aircraft, route):
    total_fuel = 0
    for seg in route:
        effective_speed = aircraft.cruise_speed + seg.wind
        hours = seg.distance_km / max(effective_speed, 1)
        fuel = hours * aircraft.fuel_burn_per_hour * (1 + seg.turbulence)
        total_fuel += fuel
    return round(total_fuel, 2)

def optimize_routes(aircraft, route_files, aircraft_file="aircraft.csv"):
    results = {}
    best_route, best_fuel = None, float("inf")

    for file in route_files:
        route = load_route(file)
        fuel = estimate_fuel(aircraft, route)
        results[file] = fuel
        if fuel < best_fuel:
            best_fuel, best_route = fuel, file

    return results, {"route": best_route, "fuel": best_fuel}
