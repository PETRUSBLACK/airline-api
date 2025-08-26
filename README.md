A **FastAPI-based service** for estimating and optimizing aircraft fuel usage across different flight routes.  

It allows users to:  
- List available aircraft  
- Estimate fuel consumption for a single aircraft + route  
- Compare multiple routes and choose the most fuel-efficient one  
- Run a **local client script (`agent_local.py`)** to interact with the API  

---

## 🚀 Getting Started

### Run with Docker
```
docker build -t airline-api .
docker run -d -p 8001:8000 airline-api


RUN LOCALLY

uvicorn app.main:app --reload
Project Structure

FastAPI/
│── app/
│   ├── main.py          # FastAPI entry point with API routes
│   ├── models.py        # Core entities: Aircraft, RouteSegment
│   ├── optimizer.py     # Fuel estimation & route optimization logic
│   └── __init__.py
│── data/
│   ├── aircraft.csv     # Example aircraft dataset
│   ├── routes.csv       # Example flight route
│   └── routes_option_*.csv  # Alternative routes
│── agent_local.py       # Local client to interact with the API
│── Dockerfile
│── requirements.txt
│── README.md


CORE COMPONENTS
models.py → Defines the data structures:

Aircraft (cruise speed, fuel burn, etc.)

RouteSegment (waypoint, distance, wind, turbulence)

optimizer.py → Business logic:

load_aircraft_data(file) → Load aircraft data from CSV

load_route(file) → Load route segments from CSV

estimate_fuel(aircraft, route) → Calculate fuel consumption

optimize_routes(...) → Compare multiple routes

main.py → API endpoints with FastAPI

API ENDPOINTS
Method	Endpoint	Description
GET	/	Welcome message & API info
GET	/aircraft	List available aircraft
GET	/estimate/{aircraft_type}/{route_file}	Estimate fuel for one route
POST	/optimize/{aircraft_type}	Compare multiple routes and pick the best one

QUICK START WITH agent_local.py

You can interact with the API locally using the client script.


python agent_local.py
It will ask for:

Aircraft type (e.g., A320)

Route CSV files (comma-separated)

Example Run:

Aircraft (e.g., A320): A320
Comma-separated route CSVs (e.g., routes.csv,routes_option_b.csv): routes.csv,routes_option_b.csv

Example Output:

Aircraft: A320
Options:
 - routes.csv: total_fuel_kg = 5120
    * WP1: 1200 kg
    * WP2: 1800 kg
    * WP3: 2120 kg
 - routes_option_b.csv: total_fuel_kg = 4980
    * WP1: 1150 kg
    * WP2: 1700 kg
    * WP3: 2130 kg

Best route: routes_option_b.csv with 4980 kg

Savings vs others:
  routes.csv: extra_vs_best_kg = 140