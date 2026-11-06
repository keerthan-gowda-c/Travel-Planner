from math import radians, sin, cos, sqrt, atan2
from .destinations import DESTINATIONS
from .transport import estimate_transport_cost
from .geocoding import get_coordinates

def calculate_distance(origin_lat, origin_lon, destination_lat, destination_lon):
    earth_radius = 6371
    lat1 = radians(origin_lat)
    lon1 = radians(origin_lon)
    lat2 = radians(destination_lat)
    lon2 = radians(destination_lon)
    lat_difference = lat2 - lat1
    lon_difference = lon2 - lon1

    a = (sin(lat_difference/2)**2 + cos(lat1) * cos(lat2) * sin(lon_difference/2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return round(earth_radius * c, 2)


def recommend_destination(
    origin,
    start_date,
    end_date,
    budget,
    travel_mode="car",
):
    coordinates = get_coordinates(origin.strip())

    if coordinates is None:
        raise ValueError(
            "Unable to find this origin. Please enter a valid Indian city."
        )

    origin_latitude = coordinates["latitude"]
    origin_longitude = coordinates["longitude"]

    total_days = (end_date - start_date).days + 1
    total_nights = (end_date - start_date).days

    if total_days <= 0:
        return []

    affordable_destinations = []

    for destination in DESTINATIONS:
        distance = calculate_distance(
            origin_latitude,
            origin_longitude,
            destination["latitude"],
            destination["longitude"],
        )

        travel_cost = estimate_transport_cost(
            distance,
            travel_mode,
        )

        stay_cost = destination["stay_per_day"] * total_nights
        food_cost = destination["food_per_day"] * total_days
        activities_cost = destination["activities_per_day"] * total_days

        total_cost = (
            travel_cost
            + stay_cost
            + food_cost
            + activities_cost
        )

        if total_cost <= budget:
            affordable_destinations.append({
                "name": destination["name"],
                "state": destination["state"],
                "region": destination["region"],
                "travel_mode": travel_mode,
                "distance_km": distance,
                "travel_cost": travel_cost,
                "stay_cost": stay_cost,
                "food_cost": food_cost,
                "activities_cost": activities_cost,
                "estimated_cost": total_cost,
                "remaining_budget": round(
                    float(budget) - total_cost, 2
                ),
            })

    affordable_destinations.sort(
        key=lambda item: item["estimated_cost"]
    )

    return affordable_destinations[:5]



def get_origin_coordinates(origin):
    coordinates = get_coordinates(origin)

    if coordinates is None:
        raise ValueError(
            "Unable to find this origin. Please enter a valid Indian city."
        )

    return (
        coordinates["latitude"],
        coordinates["longitude"],
    )