
import { useEffect, useMemo, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
    Plus,
    Search,
    MapPin,
    CalendarDays,
    Wallet,
    ArrowRight,
} from "lucide-react";
import "./TripsPage.css";

const dummyTrips = [
    {
        title: "Mysuru Weekend Trip",
        destination: "Mysuru, Karnataka",
        startDate: "2026-11-14",
        endDate: "2026-11-16",
        budget: 8000,
        spent: 5200,
        status: "Upcoming",
        image: "https://images.unsplash.com/photo-1600100397608-f0104f7e7c2b?w=800",
    },
    {
        title: "Coorg Adventure",
        destination: "Coorg, Karnataka",
        startDate: "2026-11-20",
        endDate: "2026-11-23",
        budget: 15000,
        spent: 6800,
        status: "Upcoming",
        image: "https://images.unsplash.com/photo-1511497584788-876760111969?w=800",
    },
    {
        title: "Ooty Hill Escape",
        destination: "Ooty, Tamil Nadu",
        startDate: "2026-10-10",
        endDate: "2026-10-12",
        budget: 10000,
        spent: 9500,
        status: "Completed",
        image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=800",
    },
    {
        title: "Chikmagalur Retreat",
        destination: "Chikmagalur, Karnataka",
        startDate: "2026-11-28",
        endDate: "2026-11-30",
        budget: 12000,
        spent: 0,
        status: "Scheduled",
        image: "https://images.unsplash.com/photo-1448375240586-882707db888b?w=800",
    },
];

type TripStatus = "All" | "Upcoming" | "Scheduled" | "Completed";

function TripsPage() {
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();

    const [search, setSearch] = useState(searchParams.get("search") || "");
    const [activeFilter, setActiveFilter] = useState<TripStatus>("All");

    useEffect(() => {
        setSearch(searchParams.get("search") || "");
    }, [searchParams]);


    const filteredTrips = useMemo(() => {
        return dummyTrips.filter((trip) => {
            const matchesSearch =
                trip.title.toLowerCase().includes(search.toLowerCase()) ||
                trip.destination.toLowerCase().includes(search.toLowerCase());

            const matchesFilter =
                activeFilter === "All" || trip.status === activeFilter;

            return matchesSearch && matchesFilter;
        });
    }, [search, activeFilter]);

    const formatDate = (date: string) =>
        new Date(`${date}T00:00:00`).toLocaleDateString("en-IN", {
            day: "numeric",
            month: "short",
            year: "numeric",
        });

    return (
        <div className="trips-page">
            <div className="trips-page-header">
                <div>
                    <h1>My Trips</h1>
                    <p>Manage and keep track of all your journeys.</p>
                </div>

                <button
                    className="create-trip-btn"
                    onClick={() => navigate("/trips/create")}
                >
                    <Plus size={18} />
                    Create New Trip
                </button>
            </div>

            <div className="trips-summary">
                <div>
                    <span>Total Trips</span>
                    <h2>{dummyTrips.length}</h2>
                </div>
                <div>
                    <span>Upcoming</span>
                    <h2>{dummyTrips.filter(t => t.status === "Upcoming").length}</h2>
                </div>
                <div>
                    <span>Completed</span>
                    <h2>{dummyTrips.filter(t => t.status === "Completed").length}</h2>
                </div>
                <div>
                    <span>Total Budget</span>
                    <h2>₹{dummyTrips.reduce((sum, t) => sum + t.budget, 0).toLocaleString("en-IN")}</h2>
                </div>
            </div>

            <div className="trips-toolbar">
                <div className="trips-search">
                    <Search size={18} />
                    <input
                        type="text"
                        placeholder="Search trips or destinations..."
                        value={search}
                        onChange={(e) => {
                            const value = e.target.value;

                            setSearch(value);

                            setSearchParams(
                                value.trim()
                                    ? { search: value }
                                    : {},
                                { replace: true }
                            );
                        }}
                    />
                </div>

                <div className="trip-filters">
                    {(["All", "Upcoming", "Scheduled", "Completed"] as TripStatus[]).map((filter) => (
                        <button
                            key={filter}
                            className={activeFilter === filter ? "active" : ""}
                            onClick={() => setActiveFilter(filter)}
                        >
                            {filter}
                        </button>
                    ))}
                </div>
            </div>

            <div className="trips-grid">
                {filteredTrips.map((trip) => (
                    <article className="trip-card" key={trip.title}>
                        <div className="trip-card-image">
                            <img src={trip.image} alt={trip.destination} />
                            <span className={`trip-status ${trip.status.toLowerCase()}`}>
                                {trip.status}
                            </span>
                        </div>

                        <div className="trip-card-content">
                            <h3>{trip.title}</h3>

                            <div className="trip-card-detail">
                                <MapPin size={15} />
                                {trip.destination}
                            </div>

                            <div className="trip-card-detail">
                                <CalendarDays size={15} />
                                {formatDate(trip.startDate)} – {formatDate(trip.endDate)}
                            </div>

                            <div className="trip-card-budget">
                                <div>
                                    <span>Budget</span>
                                    <strong>₹{trip.budget.toLocaleString("en-IN")}</strong>
                                </div>
                                <div>
                                    <span>Spent</span>
                                    <strong>₹{trip.spent.toLocaleString("en-IN")}</strong>
                                </div>
                            </div>

                            <button
                                className="view-trip-btn"
                                onClick={() => navigate(`/trips/${encodeURIComponent(trip.title)}`)}
                            >
                                View Details <ArrowRight size={16} />
                            </button>
                        </div>
                    </article>
                ))}
            </div>

            {filteredTrips.length === 0 && (
                <div className="trips-empty">
                    <Search size={32} />
                    <h3>No trips found</h3>
                    <p>Try another search or change your status filter.</p>
                </div>
            )}
        </div>
    );
}

export default TripsPage;
