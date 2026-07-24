import os
import requests
import openrouteservice
from .geocoding_service import get_coordinates


API_KEY = os.getenv("ORS_API_KEY")

BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_route(start, destination):

    start_coordinates = get_coordinates(start)

    destination_coordinates = get_coordinates(destination)

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
    "coordinates": [
        start_coordinates,
        destination_coordinates
    ],
    "instructions": False,
    "geometry": True,
    "geometry_simplify": False,
    "extra_info": [
        "waytype"
    ]
}

    response = requests.post(

        BASE_URL,

        json=body,

        headers=headers,
        

    )
    if response.status_code != 200:
        raise Exception(
        f"OpenRouteService Error: {response.text}"
    )

    return response.json()


def decode_geometry(encoded_geometry):

    coordinates = openrouteservice.convert.decode_polyline(
        encoded_geometry,
        is3d=False
    )

    return coordinates["coordinates"]
def parse_route(route):

    if "routes" not in route or not route["routes"]:
        raise Exception("No route found.")

    summary = route["routes"][0]["summary"]

    geometry = route["routes"][0]["geometry"]

    coordinates = decode_geometry(geometry)

    return {

        "distance_km": round(summary["distance"] / 1000, 2),

        "duration_minutes": round(summary["duration"] / 60, 2),

        "coordinates": coordinates

    }


def get_route_information(start, destination):

    route = get_route(start, destination)

    return parse_route(route)
