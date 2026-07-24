import os
import requests

API_KEY = os.getenv("ORS_API_KEY")

def reverse_geocode(longitude, latitude):

    url = "https://api.openrouteservice.org/geocode/reverse"
    headers = {
        "Authorization": API_KEY
    }
    params = {
        "point.lon": longitude,
        "point.lat": latitude
    }
    response = requests.get(
        url,
        headers=headers,
        params=params
    )
    response.raise_for_status()
    data = response.json()
    properties = data["features"][0]["properties"]
    
    return {
        "city": properties.get("locality"),
        "state": properties.get("region_a")
    }