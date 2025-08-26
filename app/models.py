from dataclasses import dataclass

@dataclass
class Aircraft:
    aircraft_type: str
    cruise_speed: float        # km/h
    fuel_burn_per_hour: float  # kg/hour

@dataclass
class RouteSegment:
    waypoint: str
    distance_km: float
    wind_kmh: float           # Positive = tailwind (helps), Negative = headwind (hurts)
    turbulence: float         # Fraction e.g., 0.05 = +5% fuel penalty

def load_aircraft_data(file_path: str = "data/aircraft.csv") -> dict:
    """
    Reads CSV file with headers:
    aircraft_type,cruise_speed,fuel_burn_per_hour
    Returns dict: { 'A320': Aircraft(...), ... }
    """
    import csv
    aircrafts = {}
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            aircrafts[row["aircraft_type"]] = Aircraft(
                row["aircraft_type"],
                float(row["cruise_speed"]),
                float(row["fuel_burn_per_hour"])
            )
    return aircrafts
