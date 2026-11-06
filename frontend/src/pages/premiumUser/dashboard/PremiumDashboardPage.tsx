
import { useNavigate } from "react-router-dom";
import {
    Plane,
    Wallet,
    TrendingUp,
    MapPin,
    Plus,
    ArrowRight,
    CalendarDays,
    Sparkles,
    Target,
    Clock,
    ChartNoAxesCombined,
} from "lucide-react";

import "./PremiumDashboardPage.css";

function PremiumDashboardPage() {
    const navigate = useNavigate();

    const stats = [
        {
            title: "Total Trips",
            value: "12",
            description: "Trips planned so far",
            icon: Plane,
        },
        {
            title: "Total Spending",
            value: "₹42,500",
            description: "Across all trips",
            icon: Wallet,
        },
        {
            title: "Budget Efficiency",
            value: "87%",
            description: "Average budget utilization",
            icon: Target,
        },
        {
            title: "Destinations",
            value: "08",
            description: "Places explored",
            icon: MapPin,
        },
    ];

    const upcomingTrips = [
        {
            title: "Mysuru Weekend",
            destination: "Mysuru",
            dates: "24 Oct – 26 Oct",
            status: "Upcoming",
        },
        {
            title: "Coorg Adventure",
            destination: "Coorg",
            dates: "12 Nov – 15 Nov",
            status: "Upcoming",
        },
    ];

    return (
        <div className="premium-dashboard">

            {/* Header */}
            <div className="premium-dashboard-header">
                <div>
                    <div className="premium-welcome-label">
                        <Sparkles size={16} />
                        PREMIUM MEMBER
                    </div>

                    <h1>Welcome Back!</h1>
                    <p>
                        Manage your journeys and make every trip count.
                    </p>
                </div>

                <button
                    className="premium-create-btn"
                    onClick={() => navigate("/trips/create")}
                >
                    <Plus size={18} />
                    Create New Trip
                </button>
            </div>

            {/* Summary Cards */}
            <div className="premium-stats-grid">
                {stats.map((stat) => {
                    const Icon = stat.icon;

                    return (
                        <div className="premium-stat-card" key={stat.title}>
                            <div className="premium-stat-top">
                                <span>{stat.title}</span>
                                <div className="premium-stat-icon">
                                    <Icon size={21} />
                                </div>
                            </div>

                            <h2>{stat.value}</h2>
                            <p>{stat.description}</p>
                        </div>
                    );
                })}
            </div>

            {/* Main Content */}
            <div className="premium-dashboard-content">

                {/* Upcoming Trips */}
                <section className="premium-section-card">
                    <div className="premium-section-header">
                        <div>
                            <h3>Upcoming Trips</h3>
                            <p>Your next planned journeys</p>
                        </div>

                        <button
                            className="premium-text-btn"
                            onClick={() => navigate("/trips")}
                        >
                            View All <ArrowRight size={16} />
                        </button>
                    </div>

                    <div className="premium-trip-list">
                        {upcomingTrips.map((trip) => (
                            <div className="premium-trip-item" key={trip.title}>
                                <div className="premium-trip-icon">
                                    <Plane size={21} />
                                </div>

                                <div className="premium-trip-info">
                                    <h4>{trip.title}</h4>
                                    <span>
                                        <MapPin size={14} />
                                        {trip.destination}
                                    </span>
                                    <span>
                                        <CalendarDays size={14} />
                                        {trip.dates}
                                    </span>
                                </div>

                                <span className="premium-trip-status">
                                    {trip.status}
                                </span>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Quick Actions */}
                <section className="premium-section-card">
                    <div className="premium-section-header">
                        <div>
                            <h3>Quick Actions</h3>
                            <p>Manage your travel plans</p>
                        </div>
                    </div>

                    <div className="premium-quick-actions">
                        <button onClick={() => navigate("/trips/create")}>
                            <Plus size={19} />
                            <span>Create a Trip</span>
                            <ArrowRight size={16} />
                        </button>

                        <button onClick={() => navigate("/trips")}>
                            <Plane size={19} />
                            <span>Explore My Trips</span>
                            <ArrowRight size={16} />
                        </button>

                        <button onClick={() => navigate("/analytics")}>
                            <ChartNoAxesCombined size={19} />
                            <span>View Analytics</span>
                            <ArrowRight size={16} />
                        </button>
                    </div>
                </section>
            </div>

            {/* Premium Insights */}
            <section className="premium-insights-section">
                <div className="premium-section-header">
                    <div>
                        <h3>
                            <Sparkles size={19} />
                            Premium Insights
                        </h3>
                        <p>Highlights from your travel activity</p>
                    </div>

                    <button
                        className="premium-text-btn"
                        onClick={() => navigate("/analytics")}
                    >
                        Detailed Analytics <ArrowRight size={16} />
                    </button>
                </div>

                <div className="premium-insights-grid">
                    <div className="premium-insight-card">
                        <div className="premium-insight-icon">
                            <Target size={20} />
                        </div>
                        <h4>Budget Performance</h4>
                        <p>
                            You have stayed within your planned budget
                            on most of your trips.
                        </p>
                    </div>

                    <div className="premium-insight-card">
                        <div className="premium-insight-icon">
                            <Wallet size={20} />
                        </div>
                        <h4>Top Expense Category</h4>
                        <p>
                            Accommodation is currently your highest
                            travel expense category.
                        </p>
                    </div>

                    <div className="premium-insight-card">
                        <div className="premium-insight-icon">
                            <Clock size={20} />
                        </div>
                        <h4>Average Daily Spending</h4>
                        <strong>₹2,125</strong>
                        <p>Your average spending per travel day.</p>
                    </div>
                </div>
            </section>

        </div>
    );
}

export default PremiumDashboardPage;
