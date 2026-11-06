
import { useNavigate, useParams } from "react-router-dom";
import {
    ArrowLeft,
    MapPin,
    CalendarDays,
    Wallet,
    Plane,
    Hotel,
    Utensils,
    Camera,
    CheckCircle2,
    Clock,
    Pencil,
} from "lucide-react";
import "./TripDetailsPage.css";

const tripData = {
    "Mysuru Weekend Trip": {
        destination: "Mysuru, Karnataka",
        dates: "14 Nov 2026 – 16 Nov 2026",
        duration: "3 Days",
        budget: 8000,
        spent: 5200,
        status: "Upcoming",
        description: "Explore the royal heritage, beautiful palaces, and cultural attractions of Mysuru.",
        stops: [
            {
                day: "Day 1",
                title: "Explore Mysuru City",
                activities: [
                    "Visit Mysore Palace",
                    "Explore Devaraja Market",
                    "Evening at Brindavan Gardens",
                ],
            },
            {
                day: "Day 2",
                title: "Nature and Heritage",
                activities: [
                    "Visit Chamundi Hills",
                    "Explore St. Philomena's Church",
                    "Visit Mysuru Zoo",
                ],
            },
            {
                day: "Day 3",
                title: "Relax and Return",
                activities: [
                    "Breakfast at a local restaurant",
                    "Visit Karanji Lake",
                    "Return to origin",
                ],
            },
        ],
    },
};

function TripDetailsPage() {
    const navigate = useNavigate();
    const { tripTitle } = useParams();

    const title = decodeURIComponent(tripTitle || "");
    const trip = tripData[title as keyof typeof tripData];

    if (!trip) {
        return (
            <div className="trip-not-found">
                <h2>Trip not found</h2>
                <p>We couldn't find the requested trip.</p>
                <button onClick={() => navigate("/trips")}>
                    Back to My Trips
                </button>
            </div>
        );
    }

    const remainingBudget = trip.budget - trip.spent;
    const spendingPercentage = (trip.spent / trip.budget) * 100;

    return (
        <div className="trip-details-page">
            <button
                className="back-to-trips"
                onClick={() => navigate("/trips")}
            >
                <ArrowLeft size={17} />
                Back to My Trips
            </button>

            <div className="trip-details-header">
                <div>
                    <span className="trip-details-status">{trip.status}</span>
                    <h1>{title}</h1>
                    <p>{trip.description}</p>
                </div>

                <button className="edit-trip-btn">
                    <Pencil size={16} />
                    Edit Trip
                </button>
            </div>

            <div className="trip-details-banner">
                <div>
                    <MapPin size={19} />
                    <span>{trip.destination}</span>
                </div>
                <div>
                    <CalendarDays size={19} />
                    <span>{trip.dates}</span>
                </div>
                <div>
                    <Clock size={19} />
                    <span>{trip.duration}</span>
                </div>
            </div>

            <div className="trip-overview-grid">
                <div className="trip-overview-card">
                    <div className="overview-icon">
                        <Wallet size={21} />
                    </div>
                    <span>Total Budget</span>
                    <h2>₹{trip.budget.toLocaleString("en-IN")}</h2>
                </div>

                <div className="trip-overview-card">
                    <div className="overview-icon">
                        <CheckCircle2 size={21} />
                    </div>
                    <span>Total Spent</span>
                    <h2>₹{trip.spent.toLocaleString("en-IN")}</h2>
                </div>

                <div className="trip-overview-card">
                    <div className="overview-icon">
                        <Wallet size={21} />
                    </div>
                    <span>Remaining Budget</span>
                    <h2>₹{remainingBudget.toLocaleString("en-IN")}</h2>
                </div>
            </div>

            <section className="trip-budget-section">
                <div className="trip-section-heading">
                    <div>
                        <h3>Budget Overview</h3>
                        <p>Track your trip expenses</p>
                    </div>
                    <strong>{Math.round(spendingPercentage)}% Used</strong>
                </div>

                <div className="trip-budget-progress">
                    <div style={{ width: `${spendingPercentage}%` }} />
                </div>

                <div className="trip-budget-labels">
                    <span>Spent: ₹{trip.spent.toLocaleString("en-IN")}</span>
                    <span>Budget: ₹{trip.budget.toLocaleString("en-IN")}</span>
                </div>
            </section>

            <section className="trip-itinerary-section">
                <div className="trip-section-heading">
                    <div>
                        <h3>Trip Itinerary</h3>
                        <p>Your planned activities for this journey</p>
                    </div>
                </div>

                <div className="trip-itinerary-list">
                    {trip.stops.map((day) => (
                        <div className="trip-day-card" key={day.day}>
                            <div className="trip-day-label">
                                <span>{day.day}</span>
                            </div>

                            <div className="trip-day-content">
                                <h4>{day.title}</h4>

                                {day.activities.map((activity, index) => (
                                    <div className="trip-activity" key={index}>
                                        <span className="activity-dot" />
                                        <p>{activity}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </section>

            <section className="trip-expense-categories">
                <div className="trip-section-heading">
                    <div>
                        <h3>Expense Categories</h3>
                        <p>Sample spending breakdown</p>
                    </div>
                </div>

                <div className="expense-category-grid">
                    <div>
                        <Hotel size={20} />
                        <span>Accommodation</span>
                        <strong>₹2,000</strong>
                    </div>
                    <div>
                        <Utensils size={20} />
                        <span>Food</span>
                        <strong>₹1,200</strong>
                    </div>
                    <div>
                        <Plane size={20} />
                        <span>Transport</span>
                        <strong>₹1,500</strong>
                    </div>
                    <div>
                        <Camera size={20} />
                        <span>Activities</span>
                        <strong>₹500</strong>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default TripDetailsPage;
