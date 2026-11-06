// import { useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";
// import { ArrowLeft, CalendarDays, MapPin, Wallet } from "lucide-react";
// import type { UserProfile } from "../../types/auth";
// import { getUserProfile } from "../../services/authService";
// import { type RecommendedDestination, type TravelMode } from "../../types/recommendation";
// import { getDestinationRecommendations } from "../../services/recommendationService";
// import "./CreateTripPage.css";

// export default function CreateTripPage() {
//     const navigate = useNavigate();
//     const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
//     const [profileLoading, setProfileLoading] = useState(true)
//     const isPremium = userProfile?.subscription.plan === "premium" && userProfile?.subscription.status === "active"

//     const [origin, setOrigin] = useState("");
//     const [startDate, setStartDate] = useState("");
//     const [endDate, setEndDate] = useState("");
//     const [budget, setBudget] = useState("");
//     const [travelMode, setTravelMode] = useState<TravelMode>("train");

//     const [recommendations, setRecommendations] = useState<RecommendedDestination[]>([])
//     const [recommendationLoading, setRecommendationLoading] = useState(false)
//     const [recommendationError, setRecommendationError] = useState("")
//     const [selectedDestination, setSelectedDestination] = useState("")
//     const [hasSearched, setHasSearched] = useState(false);

//     useEffect(() => {
//         const fetchProfile = async () => {
//             try {
//                 const profile = await getUserProfile();
//                 setUserProfile(profile);
//             }
//             catch (error) {
//                 console.error("Failed to fetch user profile", error);
//             } finally {
//                 setProfileLoading(false)
//             }
//         }
//         fetchProfile();
//     }, [])

//     useEffect(() => {
//         setRecommendations([]);
//         setRecommendationError("");
//         setSelectedDestination("");
//     }, [origin, startDate, endDate, budget, travelMode]);

//     const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
//         e.preventDefault();

//         if (!selectedDestination.trim()) {
//             return;
//         }

//         const tripData = { origin: origin.trim(), destination: selectedDestination.trim(), start_date: startDate, end_date: endDate, budget: Number(budget), travel_mode: travelMode }
//         console.log(tripData);
//     }

//     const handleFindDestinations = async () => {
//         if (!isPremium) return;

//         if (!origin || !startDate || !endDate || !budget) {
//             setRecommendationError("Please complete all trip details.");
//             return
//         }

//         setRecommendationLoading(true);
//         setRecommendationError("");
//         setRecommendations([]);
//         setHasSearched(false);

//         try {
//             const response = await getDestinationRecommendations({
//                 origin: origin.trim(),
//                 start_date: startDate,
//                 end_date: endDate,
//                 budget: Number(budget),
//                 travel_mode: travelMode
//             })
//             setRecommendations(response.recommendations);
//             setHasSearched(true);
//         } catch (error: any) {
//             setRecommendationError(error.response?.data?.detail || "Unable to find destinations. Please try again.")
//         } finally {
//             setRecommendationLoading(false);
//         }
//     }

//     return (
//         <div className="create-trip-page">
//             <button className="back-button" onClick={() => navigate("/trips")}>
//                 <ArrowLeft size={18} />Back to Trips
//             </button>

//             <div className="create-trip-heading">
//                 <h1>Plan Your Next Trip</h1>
//                 <p>Tell us your travel preferences. We'll find a destination that fits your budget.</p>
//             </div>

//             <form className="create-trip-form" onSubmit={handleSubmit}>
//                 <div className="form-group">
//                     <label htmlFor="origin">
//                         <MapPin size={17} /> Starting Location
//                     </label>
//                     <input type="text" id="origin" placeholder="Enter your starting city" value={origin} onChange={(e) => setOrigin(e.target.value)} required />
//                 </div>

//                 <div className="form-row">
//                     <div className="form-group">
//                         <label htmlFor="start-date">
//                             <CalendarDays size={17} />
//                             Start Date
//                         </label>
//                         <input type="date"
//                             id="start-date"
//                             value={startDate}
//                             min={new Date().toISOString().split("T")[0]}
//                             onChange={(e) => setStartDate(e.target.value)}
//                             required />
//                     </div>

//                     <div className="form-group">
//                         <label htmlFor="end-date">
//                             <CalendarDays size={17} />
//                             End Date
//                         </label>
//                         <input
//                             id="end-date"
//                             type="date"
//                             value={endDate}
//                             min={startDate || new Date().toISOString().split("T")[0]}
//                             onChange={(e) => setEndDate(e.target.value)}
//                             required
//                         />
//                     </div>
//                 </div>

//                 <div className="form-group">
//                     <label htmlFor="budget">
//                         <Wallet size={17} />
//                         Total Budget (INR)
//                     </label>
//                     <input
//                         id="budget"
//                         type="number"
//                         min="1"
//                         placeholder="Example: 10000"
//                         value={budget}
//                         onChange={(e) => setBudget(e.target.value)}
//                         required
//                     />
//                 </div>

//                 <div className="form-group">
//                     <label htmlFor="destination">
//                         <MapPin size={17} />
//                         Destination
//                     </label>

//                     <input
//                         type="text"
//                         id="destination"
//                         placeholder="Enter your destination"
//                         value={selectedDestination}
//                         onChange={(e) => setSelectedDestination(e.target.value)}
//                         required
//                     />
//                 </div>

//                 <div className="form-group">
//                     <label htmlFor="travel-mode">Transportation Mode</label>
//                     <select id="travel-mode"
//                         value={travelMode}
//                         onChange={(e) => setTravelMode(e.target.value as TravelMode)} required>
//                         <option value="train">Train</option>
//                         <option value="bus">Bus</option>
//                         <option value="car">Car</option>
//                         <option value="flight">Flight</option>
//                     </select>
//                 </div>

//                 <div className="destination-info">
//                     <MapPin size={20} />
//                     <div>
//                         <h4>Destination Recommendation</h4>
//                         {profileLoading ?
//                             (
//                                 <p>Checking your subscription...</p>
//                             ) : isPremium ? (
//                                 <p>
//                                     Your Premium plan allows you to discover up to
//                                     five destinations based on your budget.
//                                 </p>
//                             ) : (
//                                 <p>
//                                     Destination recommendations are available
//                                     with Premium. You can still choose your own
//                                     destination with the Free plan.
//                                 </p>
//                             )
//                         }
//                     </div>
//                 </div>

//                 {isPremium && (
//                     <button type="button"
//                         className="generate-trip-button"
//                         onClick={handleFindDestinations}
//                         disabled={recommendationLoading || profileLoading}
//                     >
//                         {recommendationLoading ? "Finding Destinations..." : "Find My Destinations"}
//                     </button>
//                 )}
//                 {recommendationError && (
//                     <p className="recommendation-error">{recommendationError}</p>
//                 )}

//                 {recommendations.length > 0 && (
//                     <div className="recommendation-results">
//                         <h3>Recommended Destinations</h3>
//                         <p>Choose the destination that suits your travel plans.</p>

//                         <div className="recommendation-list">
//                             {recommendations.map((destination) => (
//                                 <div key={destination.name}
//                                     className={`recommendation-card ${selectedDestination === destination.name ? "selected" : ""}`}>
//                                     <div className="recommendation-card-header">
//                                         <div>
//                                             <h4>{destination.name}</h4>
//                                             <p>{destination.state} · {destination.region}</p>
//                                         </div>
//                                         <span>{destination.distance_km.toLocaleString("en-IN")}km</span>
//                                     </div>
//                                     <div className="recommendation-cost">
//                                         <h3>₹{destination.estimated_cost.toLocaleString("en-IN")}</h3>
//                                         <span>Estimated total cost</span>
//                                     </div>

//                                     <div className="recommendation-breakdown">
//                                         <p>Transport <span>₹{destination.travel_cost.toLocaleString("en-IN")}</span></p>
//                                         <p>Accommodation <span>₹{destination.stay_cost.toLocaleString("en-IN")}</span></p>
//                                         <p>Food <span>₹{destination.food_cost.toLocaleString("en-IN")}</span></p>
//                                         <p>Activities <span>₹{destination.activities_cost.toLocaleString("en-IN")}</span></p>
//                                         <p>Remaining budget <span>₹{destination.remaining_budget.toLocaleString("en-IN")}</span></p>

//                                     </div>
//                                     <button
//                                         type="button"
//                                         onClick={() => setSelectedDestination(destination.name)}
//                                     >
//                                         {selectedDestination === destination.name
//                                             ? "Selected"
//                                             : "Choose Destination"}
//                                     </button>

//                                 </div>
//                             ))}
//                         </div>
//                     </div>



//                 )}

//                 {hasSearched && recommendations.length === 0 && (
//                     <p className="recommendation-empty">
//                         No destinations found within your budget.
//                         Try increasing your budget or changing your travel preferences.
//                     </p>
//                 )}

//                 <button
//                     type="submit"
//                     className="generate-trip-button"
//                 >
//                     Continue to Create Trip
//                 </button>
//             </form>

//         </div>
//     )
// }


import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
    ArrowLeft,
    CalendarDays,
    MapPin,
    Wallet,
} from "lucide-react";
import "./CreateTripPage.css";

export default function CreateTripPage() {
    const navigate = useNavigate();

    const [origin, setOrigin] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [budget, setBudget] = useState("");
    const [destination, setDestination] = useState("");
    const [travelMode, setTravelMode] = useState("train");

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const tripData = {
            origin,
            destination,
            start_date: startDate,
            end_date: endDate,
            budget: Number(budget),
            travel_mode: travelMode,
        };

        console.log("Trip Details:", tripData);
    };

    return (
        <div className="create-trip-page">
            <button
                className="back-button"
                onClick={() => navigate("/trips")}
            >
                <ArrowLeft size={18} />
                Back to Trips
            </button>

            <div className="create-trip-heading">
                <h1>Plan Your Next Trip</h1>
                <p>
                    Tell us your travel preferences. We'll help you
                    plan a trip that fits your budget.
                </p>
            </div>

            <form
                className="create-trip-form"
                onSubmit={handleSubmit}
            >
                <div className="form-group">
                    <label htmlFor="origin">
                        <MapPin size={17} />
                        Starting Location
                    </label>
                    <input
                        type="text"
                        id="origin"
                        placeholder="Enter your starting city"
                        value={origin}
                        onChange={(e) => setOrigin(e.target.value)}
                        required
                    />
                </div>

                <div className="form-row">
                    <div className="form-group">
                        <label htmlFor="start-date">
                            <CalendarDays size={17} />
                            Start Date
                        </label>
                        <input
                            type="date"
                            id="start-date"
                            min={new Date().toISOString().split("T")[0]}
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="end-date">
                            <CalendarDays size={17} />
                            End Date
                        </label>
                        <input
                            type="date"
                            id="end-date"
                            min={startDate || new Date().toISOString().split("T")[0]}
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            required
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="budget">
                        <Wallet size={17} />
                        Total Budget (INR)
                    </label>
                    <input
                        type="number"
                        id="budget"
                        min="1"
                        placeholder="Example: 10000"
                        value={budget}
                        onChange={(e) => setBudget(e.target.value)}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="destination">
                        <MapPin size={17} />
                        Destination
                    </label>
                    <input
                        type="text"
                        id="destination"
                        placeholder="Enter your destination"
                        value={destination}
                        onChange={(e) => setDestination(e.target.value)}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="travel-mode">
                        Transportation Mode
                    </label>
                    <select
                        id="travel-mode"
                        value={travelMode}
                        onChange={(e) => setTravelMode(e.target.value)}
                        required
                    >
                        <option value="train">Train</option>
                        <option value="bus">Bus</option>
                        <option value="car">Car</option>
                        <option value="flight">Flight</option>
                    </select>
                </div>

                <div className="destination-info">
                    <MapPin size={20} />
                    <div>
                        <h4>Plan Your Destination</h4>
                        <p>
                            Choose your preferred destination and
                            transportation mode to get started with
                            your travel plan.
                        </p>
                    </div>
                </div>

                <button
                    type="submit"
                    className="generate-trip-button"
                >
                    Create Trip
                </button>
            </form>
        </div>
    );
}
