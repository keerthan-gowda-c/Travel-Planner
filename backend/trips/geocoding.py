import requests
from functools import lru_cache


@lru_cache(maxsize=200)
def get_coordinates(city):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q" : f"{city}, India",
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "in",
    }

    headers = {"User-Agent":"TravelPlanner/1.0 ckgowda9741@gmail.com"}

    try:
        response = requests.get(url,params=params, headers=headers,timeout=10)
        response.raise_for_status()
        results = response.json()

        if not results:
            return None

        return {
            "latitude": float(results[0]["lat"]),
            "longitude": float(results[0]["lon"]),
        }
    except requests.RequestException:
        return None