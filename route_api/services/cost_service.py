VEHICLE_MPG = 10

def calculate_fuel_cost(distance_miles, price_per_gallon):
    gallons = distance_miles / VEHICLE_MPG
    total_cost = gallons * price_per_gallon
    return {
        "gallons": round(gallons, 2),
        "fuel_cost": round(total_cost, 2)
    }