
from .destinations import DESTINATIONS


def recommend_destination(origin, start_date, end_date, budget):
    total_days = (end_date - start_date).days + 1
    total_nights = (end_date - start_date).days

    if total_days <= 0:
        return None

    affordable_destinations = []

    for destination in DESTINATIONS:
        travel_cost = destination["travel_costs"].get(
            origin.strip().title()
        )

        if travel_cost is None:
            continue

        total_cost = (
            travel_cost
            + destination["stay_per_day"] * total_nights
            + destination["food_per_day"] * total_days
            + destination["activities_per_day"] * total_days
        )

        if total_cost <= budget:
            affordable_destinations.append({
                "name": destination["name"],
                "estimated_cost": total_cost,
                "remaining_budget": float(budget) - total_cost,
            })

    if not affordable_destinations:
        return None

    affordable_destinations.sort(
        key=lambda item: item["estimated_cost"]
    )

    return affordable_destinations[0]
