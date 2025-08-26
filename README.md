# ✈️ Airline Fuel Optimization API

A **FastAPI-based service** for estimating and optimizing aircraft fuel usage across different flight routes.  
It allows users to:  
- List available aircraft data  
- Estimate fuel consumption for a single aircraft + route  
- Compare multiple routes and choose the most fuel-efficient one  

---

## 🚀 Getting Started

### Run with Docker
```bash
docker run -d -p 8001:8000 airline-api
```

### Run Normally (Development)
```bash
uvicorn app.main:app --reload
```

### Build Docker Image
```bash
docker build -t airline-api .
```

---

## 📂 Project Structure

```
FastAPI/
│── app/
│   ├── main.py          # FastAPI entry point with API routes
│   ├── models.py        # Core entities: Aircraft, RouteSegment
│   ├── optimizer.py     # Fuel estimation & route optimization logic
│   └── __init__.py
│
│── data/
│   ├── aircraft.csv     # Example aircraft dataset
│   ├── routes.csv       # Example flight route
│   └── routes_option_*.csv  # Alternative route files
│
│── Dockerfile
│── requirements.txt
│── README.md
```

---

## 🛠️ Core Components

### **models.py**
Defines the **data structures** used in the system.

- **Aircraft** → Stores aircraft performance parameters (cruise speed, fuel burn per hour).  
- **RouteSegment** → Stores details of a segment in a flight route (distance, wind, turbulence).

---

### **optimizer.py**
Contains the **business logic** for the app.

#### Functions

- **`load_aircraft_data(file_path)`**  
  Reads aircraft data from CSV.  
  Returns → `{aircraft_type: Aircraft(...)}`
  
- **`load_route(file_path)`**  
  Reads route segments from CSV.  
  Returns → list of `RouteSegment` objects  

- **`estimate_fuel(aircraft, route)`**  
  Calculates total fuel consumption for a given aircraft on a route.  
  Considers:  
  - Cruise speed adjusted for wind  
  - Turbulence as a multiplier  
  Returns → Rounded fuel in kg  

- **`optimize_routes(aircraft, route_files, aircraft_file)`**  
  Compares multiple routes for the same aircraft.  
  Returns →  
  - Fuel estimates per route  
  - The **best (lowest fuel)** route  

🔹 **Role:** Encapsulates all the core business logic (data loading, calculation, optimization).  
🔹 **Uses:** `Aircraft` and `RouteSegment` classes from `models.py` for structured calculations.  

---

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Welcome message & API info |
| `GET`  | `/aircraft` | List available aircraft data |
| `GET`  | `/estimate/{aircraft_type}/{route_file}` | Estimate fuel for one aircraft & one route |
| `POST` | `/optimize/{aircraft_type}` | Compare multiple routes for a given aircraft |

---

## 🔎 Example Usage

### Estimate Fuel (Single Route)
**Request:**  
```
GET /estimate/A320/routes.csv
```

**Response:**  
```json
{
  "aircraft": "A320",
  "route_file": "routes.csv",
  "estimated_fuel_kg": 5120
}
```

---

### Optimize Fuel (Multiple Routes)
**Request:**  
```
POST /optimize/A320
```

**Body (JSON):**
```json
[
  "routes.csv",
  "routes_option_b.csv",
  "routes_option_c.csv"
]
```

**Response:**  
```json
{
  "aircraft": "A320",
  "results": {
    "routes.csv": 5120,
    "routes_option_b.csv": 4980,
    "routes_option_c.csv": 5300
  },
  "best_route": "routes_option_b.csv",
  "fuel_saved_kg": 140
}
```

---
