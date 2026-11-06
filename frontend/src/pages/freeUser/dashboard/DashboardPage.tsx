
import {
    Plane,
    Wallet,
    MapPin,
    Activity,
    Plus,
    ArrowRight,
    CalendarDays,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import "./DashboardPage.css";

function DashboardPage() {
    const navigate = useNavigate();

    return (
        <div className="dashboard-page">

            {/* Heading */}
            <div className="dashboard-heading">
                <div>
                    <h1>Welcome Back!</h1>
                    <p>Here's an overview of your travel activities.</p>
                </div>

                <button
                    className="dashboard-create-button"
                    onClick={() => navigate("/trips/create")}
                >
                    <Plus size={18} />
                    Plan New Trip
                </button>
            </div>

            {/* Statistics */}
            <div className="dashboard-stats">

                <div className="dashboard-stat-card">
                    <div className="dashboard-stat-icon blue">
                        <Plane size={22} />
                    </div>
                    <p>Total Trips</p>
                    <h2>08</h2>
                    <span>Trips created</span>
                </div>

                <div className="dashboard-stat-card">
                    <div className="dashboard-stat-icon green">
                        <Wallet size={22} />
                    </div>
                    <p>Total Budget</p>
                    <h2>₹45,000</h2>
                    <span>Across all trips</span>
                </div>

                <div className="dashboard-stat-card">
                    <div className="dashboard-stat-icon purple">
                        <MapPin size={22} />
                    </div>
                    <p>Destinations</p>
                    <h2>06</h2>
                    <span>Places explored</span>
                </div>

                <div className="dashboard-stat-card">
                    <div className="dashboard-stat-icon orange">
                        <Activity size={22} />
                    </div>
                    <p>Active Trips</p>
                    <h2>02</h2>
                    <span>Currently active</span>
                </div>

            </div>

            {/* Main Content */}
            <div className="dashboard-content-grid">

                {/* Upcoming Trips */}
                <div className="dashboard-section">
                    <div className="dashboard-section-heading">
                        <div>
                            <h3>Upcoming Trips</h3>
                            <p>Your next planned journeys.</p>
                        </div>

                        <button onClick={() => navigate("/trips")}>
                            View All <ArrowRight size={15} />
                        </button>
                    </div>

                    <div className="dashboard-trip-list">

                        <div className="dashboard-trip-item">
                            <div className="dashboard-trip-icon">
                                <MapPin size={21} />
                            </div>

                            <div className="dashboard-trip-info">
                                <h4>Mysuru Weekend</h4>
                                <span>
                                    <CalendarDays size={14} />
                                    24 Oct – 26 Oct
                                </span>
                            </div>

                            <span className="trip-status upcoming">
                                Upcoming
                            </span>
                        </div>

                        <div className="dashboard-trip-item">
                            <div className="dashboard-trip-icon">
                                <MapPin size={21} />
                            </div>

                            <div className="dashboard-trip-info">
                                <h4>Coorg Adventure</h4>
                                <span>
                                    <CalendarDays size={14} />
                                    12 Nov – 15 Nov
                                </span>
                            </div>

                            <span className="trip-status upcoming">
                                Upcoming
                            </span>
                        </div>

                    </div>
                </div>

                {/* Quick Actions */}
                <div className="dashboard-section dashboard-quick-section">
                    <h3>Quick Actions</h3>
                    <p>What would you like to do today?</p>

                    <button
                        className="quick-action-button"
                        onClick={() => navigate("/trips/create")}
                    >
                        <Plus size={18} />
                        Create a New Trip
                        <ArrowRight size={17} />
                    </button>

                    <button
                        className="quick-action-button"
                        onClick={() => navigate("/trips")}
                    >
                        <Plane size={18} />
                        Explore My Trips
                        <ArrowRight size={17} />
                    </button>

                    <button
                        className="quick-action-button"
                        onClick={() => navigate("/analytics")}
                    >
                        <Wallet size={18} />
                        View Analytics
                        <ArrowRight size={17} />
                    </button>
                </div>

            </div>

            {/* Recent Trips */}
            <div className="dashboard-section dashboard-recent-section">
                <div className="dashboard-section-heading">
                    <div>
                        <h3>Recent Trips</h3>
                        <p>Your recently created journeys.</p>
                    </div>

                    <button onClick={() => navigate("/trips")}>
                        View All <ArrowRight size={15} />
                    </button>
                </div>

                <div className="dashboard-recent-empty">
                    <Plane size={30} />
                    <h4>No recent trips to display</h4>
                    <p>Your created trips will appear here.</p>
                </div>
            </div>

        </div>
    );
}

export default DashboardPage;
