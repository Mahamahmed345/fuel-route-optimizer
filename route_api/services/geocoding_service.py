import os
import requests

API_KEY = os.getenv("ORS_API_KEY")

def get_coordinates(place):

    url = "https://api.openrouteservice.org/geocode/search"
    headers = {
        "Authorization": API_KEY
    }
    params = {
        "text": place,
        "size": 1
    }
    response = requests.get(
        url,
        headers=headers,
        params=params
    )
    data = response.json()
    if not data["features"]:
        raise ValueError(f"Location '{place}' not found.")
    coordinates = data["features"][0]["geometry"]["coordinates"]

    return coordinates