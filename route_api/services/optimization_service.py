from .routing_service import get_route_information
from .location_service import reverse_geocode
from .fuel_service import find_cheapest_station
from .cost_service import calculate_fuel_cost
from geopy.distance import geodesic

MAX_RANGE_MILES = 500

def km_to_miles(km):
    return km * 0.621371

def calculate_stop_distances(total_distance_miles):

    stop_distances = []

    current_distance = MAX_RANGE_MILES

    while current_distance < total_distance_miles:

        stop_distances.append(current_distance)

        current_distance += MAX_RANGE_MILES

    return stop_distances

def get_stop_coordinates(coordinates, stop_distances):

    stop_coordinates = []

    current_stop_index = 0

    cumulative_distance = 0

    for i in range(1, len(coordinates)):

        previous = (
            coordinates[i - 1][1],
            coordinates[i - 1][0]
        )

        current = (
            coordinates[i][1],
            coordinates[i][0]
        )

        segment_distance = geodesic(
            previous,
            current
        ).miles

        cumulative_distance += segment_distance

        if (
            current_stop_index < len(stop_distances)
            and cumulative_distance >= stop_distances[current_stop_index]
        ):

            stop_coordinates.append(
                coordinates[i]
            )

            current_stop_index += 1

    return stop_coordinates

def calculate_leg_distances(total_distance_miles, stop_distances):

    legs = []

    previous_stop = 0

    for stop in stop_distances:

        legs.append(stop - previous_stop)

        previous_stop = stop

    remaining = total_distance_miles - previous_stop

    if remaining > 0:
        legs.append(remaining)

    return legs

def optimize_route(start, destination):

    route = get_route_information(start, destination)

    total_distance = km_to_miles(route["distance_km"])

    stop_distances = calculate_stop_distances(total_distance)

    stop_coordinates = get_stop_coordinates(
        route["coordinates"],
        stop_distances
    )
    
    leg_distances = calculate_leg_distances(
    total_distance,
    stop_distances
)

    fuel_stops = []

    for i, coordinate in enumerate(stop_coordinates):

        longitude = coordinate[0]
        latitude = coordinate[1]
        

        location = reverse_geocode(longitude, latitude)

        station = find_cheapest_station(
            city=location["city"],
            state=location["state"]
        )

        if station:
            fuel_distance = leg_distances[min(i + 1, len(leg_distances) - 1)]

            cost = calculate_fuel_cost(
                fuel_distance,
                station["Retail Price"]
            )
            fuel_stops.append({

    "stop_number": len(fuel_stops) + 1,

    "stop_location": {
        "city": location["city"],
        "state": location["state"],
        "longitude": round(longitude, 6),
        "latitude": round(latitude, 6)
    },

    "match_type": station["match_type"],

    "station": {
        "truckstop_name": station["Truckstop Name"],
        "address": station["Address"],
        "city": station["City"],
        "state": station["State"],
        "retail_price_per_gallon": station["Retail Price"]
    },

    "fuel": {
        "distance_to_next_stop_miles": round(
            fuel_distance,
            2
        ),
        "gallons": cost["gallons"],
        "fuel_cost": cost["fuel_cost"]
    }

})

    total_cost = sum(
        stop["fuel"]["fuel_cost"]
        for stop in fuel_stops
    )

    total_gallons = sum(
        stop["fuel"]["gallons"]
        for stop in fuel_stops
    )

    return {

    "trip": {

        "start": start,

        "destination": destination,

        "distance_miles": round(total_distance, 2),

        "distance_km": round(route["distance_km"], 2),

        "estimated_duration_minutes": round(
            route["duration_minutes"],
            2
        ),

        "vehicle": {

            "fuel_efficiency_mpg": 10,

            "maximum_range_miles": 500

        }

    },

    "summary": {

        "number_of_stops": len(fuel_stops),

        "total_fuel_consumed_gallons": round(
            total_gallons,
            2
        ),

        "total_fuel_cost": round(
            total_cost,
            2
        )

    },

    "fuel_stops": fuel_stops

}