import csv
import os
from typing import List, Dict
from app.models import Aircraft, RouteSegment, load_aircraft_data

def load_route(file_path: str) -> List[RouteSegment]:
    """
    Reads CSV:
    waypoint,distance_km,wind,turbulence
    Returns list[RouteSegment]
    """
    segments = []
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            segments.append(
                RouteSegment(
                    row["waypoint"],
                    float(row["distance_km"]),
                    float(row["wind"]),
                    float(row["turbulence"])
                )
            )
    return segments

def estimate_fuel(aircraft: Aircraft, route: List[RouteSegment]) -> Dict:
    """
    Returns:
    {
      "total_fuel": 12345.67,
      "segments": [
         {"waypoint":"Lagos","distance_km":..., "fuel": ...}, ...
      ]
    }
    Calculation per segment:
      effective_speed = aircraft.cruise_speed + wind_kmh
      time_hours = distance_km / max(effective_speed, 100)
      base_fuel = time_hours * fuel_burn_per_hour
      final_fuel = base_fuel * (1 + turbulence)
    """
    total = 0.0
    breakdown = []
    for seg in route:
        eff_speed = aircraft.cruise_speed + seg.wind_kmh
        if eff_speed < 100:
            eff_speed = 100.0
        hours = seg.distance_km / eff_speed
        base = hours * aircraft.fuel_burn_per_hour
        final = base * (1.0 + seg.turbulence)
        breakdown.append({
            "waypoint": seg.waypoint,
            "distance_km": seg.distance_km,
            "wind_kmh": seg.wind_kmh,
            "turbulence": seg.turbulence,
            "fuel_kg": round(final, 2)
        })
        total += final

    return {"total_fuel": round(total, 2), "segments": breakdown}

def optimize_routes(aircraft_type: str, route_files: List[str], aircraft_file: str = "data/aircraft.csv") -> Dict:
    """
    Compare multiple CSV routes for an aircraft.
    Returns detailed options + best route info.
    Skips missing files and reports them.
    """
    aircrafts = load_aircraft_data(aircraft_file)
    if aircraft_type not in aircrafts:
        return {"error": f"Aircraft {aircraft_type} not found"}

    aircraft = aircrafts[aircraft_type]
    results = []
    for rf in route_files:
        path = os.path.join("data", rf)
        if not os.path.exists(path):
            results.append({"route_file": rf, "error": "File not found"})
            continue
        route = load_route(path)
        estimation = estimate_fuel(aircraft, route)
        results.append({
            "route_file": rf,
            "total_fuel": estimation["total_fuel"],
            "segments": estimation["segments"]
        })

    # Find best among those with numeric total_fuel
    numeric = [r for r in results if "total_fuel" in r]
    if not numeric:
        return {"aircraft": aircraft_type, "options": results, "best": None}

    best = min(numeric, key=lambda x: x["total_fuel"])
    # compute savings vs best
    for r in numeric:
        r["extra_vs_best_kg"] = round(r["total_fuel"] - best["total_fuel"], 2)
    return {
        "aircraft": aircraft_type,
        "options": results,
        "best": best,
        "best_total_fuel": best["total_fuel"]
    }
