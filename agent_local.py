# agent_local.py
import requests
import json

API_BASE = "http://localhost:8000"

def estimate(aircraft, route_file):
    r = requests.get(f"{API_BASE}/estimate/{aircraft}/{route_file}")
    r.raise_for_status()
    return r.json()

def optimize(aircraft, route_files):
    r = requests.post(f"{API_BASE}/optimize/{aircraft}", json={"files": route_files})
    r.raise_for_status()
    return r.json()

def pretty_print_optimize(result):
    print("Aircraft:", result.get("aircraft"))
    print("Options:")
    for opt in result.get("options", []):
        if "error" in opt:
            print(f" - {opt['route_file']}: ERROR: {opt['error']}")
        else:
            print(f" - {opt['route_file']}: total_fuel_kg = {opt['total_fuel']}")
            for seg in opt["segments"]:
                print(f"    * {seg['waypoint']}: {seg['fuel_kg']} kg")

    best = result.get("best")
    if best:
        print("\nBest route:", best["route_file"], "with", best["total_fuel"], "kg")
        print("\nSavings vs others:")
        for opt in result.get("options", []):
            if "total_fuel" in opt:
                print(f"  {opt['route_file']}: extra_vs_best_kg = {round(opt['total_fuel'] - best['total_fuel'],2)}")

if __name__ == "__main__":
    # Example: interactive
    aircraft = input("Aircraft (e.g., A320): ").strip()
    files = input("Comma-separated route CSVs (e.g., routes.csv,routes_option_b.csv): ").strip().split(",")
    files = [f.strip() for f in files if f.strip()]
    if len(files) == 1:
        res = estimate(aircraft, files[0])
        print(json.dumps(res, indent=2))
    else:
        res = optimize(aircraft, files)
        pretty_print_optimize(res)
