
TRANSPORT_MODES = {
    "train": {
        "label": "Train",
        "cost_per_km": 1.5,
        "distance_factor": 1.15,
    },
    "bus": {
        "label": "Bus",
        "cost_per_km": 2.0,
        "distance_factor": 1.10,
    },
    "car": {
        "label": "Car",
        "cost_per_km": 12.0,
        "distance_factor": 1.20,
    },
    "flight": {
        "label": "Flight",
        "cost_per_km": 5.0,
        "distance_factor": 1.0,
    },
}


def estimate_transport_cost(distance_km, travel_mode):
    if not isinstance(distance_km, (int, float)) or distance_km <= 0:
        raise ValueError("Distance must be a positive number.")

    if not isinstance(travel_mode, str):
        raise ValueError("Travel mode must be a string.")

    mode = travel_mode.strip().lower()

    if mode not in TRANSPORT_MODES:
        raise ValueError("Invalid transportation mode.")

    transport = TRANSPORT_MODES[mode]

    estimated_distance = distance_km * transport["distance_factor"]

    # Estimate round-trip transportation cost
    total_cost = (
        estimated_distance
        * transport["cost_per_km"]
        * 2
    )

    return round(total_cost)
