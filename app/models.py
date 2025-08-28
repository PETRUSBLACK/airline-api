class Aircraft:
    def __init__(self, aircraft_type, cruise_speed, fuel_burn_per_hour):
        self.aircraft_type = aircraft_type
        self.cruise_speed = cruise_speed
        self.fuel_burn_per_hour = fuel_burn_per_hour

class RouteSegment:
    def __init__(self, waypoint, distance_km, wind, turbulence):
        self.waypoint = waypoint
        self.distance_km = distance_km
        self.wind = wind
        self.turbulence = turbulence
