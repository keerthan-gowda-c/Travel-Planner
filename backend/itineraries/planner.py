
ITINERARY_PLANS = {
    "Mysuru": [
        {
            "title": "Explore Mysuru Palace",
            "description": "Visit the palace and explore the surrounding area.",
            "estimated_cost": 200,
        },
        {
            "title": "Visit Chamundi Hills",
            "description": "Enjoy the hilltop views and visit the temple.",
            "estimated_cost": 100,
        },
        {
            "title": "Explore Brindavan Gardens",
            "description": "Spend time exploring the gardens.",
            "estimated_cost": 150,
        },
    ],
    "Chikkamagaluru": [
        {
            "title": "Explore Coffee Estates",
            "description": "Discover the local coffee-growing region.",
            "estimated_cost": 300,
        },
        {
            "title": "Visit Mullayanagiri",
            "description": "Explore the mountain area and enjoy the views.",
            "estimated_cost": 200,
        },
        {
            "title": "Explore the Town",
            "description": "Visit local attractions and try regional food.",
            "estimated_cost": 150,
        },
    ],
    "Hassan": [
        {
            "title": "Visit Belur",
            "description": "Explore the historic temple architecture.",
            "estimated_cost": 150,
        },
        {
            "title": "Visit Halebidu",
            "description": "Discover the area's historic monuments.",
            "estimated_cost": 150,
        },
        {
            "title": "Explore Hassan",
            "description": "Explore local attractions and markets.",
            "estimated_cost": 100,
        },
    ],
}


def generate_itinerary(trip):
    activities = ITINERARY_PLANS.get(trip.destination)

    if not activities:
        return []

    total_days = (trip.end_date - trip.start_date).days
    itinerary = []

    for day in range(1, total_days+1):
        activity = activities[(day -1) % len(activities)]

        itinerary.append({
            "trip":trip,
            "day_number":day,
            "title":activity["title"],
            "description":activity["description"],
            "estimated_cost":activity["estimated_cost"]
        })

    return itinerary