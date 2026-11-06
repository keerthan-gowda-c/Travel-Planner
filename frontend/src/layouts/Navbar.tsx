import { useNavigate } from "react-router-dom";
import "./Navbar.css";
import { Bell, CircleUserRound, Crown } from "lucide-react";
import { useEffect, useState } from "react";
import type { UserProfile } from "../types/auth";
import { getUserProfile } from "../services/authService";


export default function Navbar() {

    const navigate = useNavigate();

    const [profile, setProfile] = useState<UserProfile | null>(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await getUserProfile();
                setProfile(data);
            } catch (error) {
                console.error("Failed to fetch user profile:", error)
            }
        }
        fetchProfile();
    }, [])

    const isPremium = profile?.subscription.plan === "premium" && profile?.subscription.status === "active";

   

    return (
        <header className="topbar">
            <div className="navbar-actions">
                <button className="notification-button" aria-label="Notification">
                    <Bell size={18} />
                    <span className="notification-dot"></span>
                </button>


                <button type="button" className="navbar-profile" onClick={() => navigate("/profile")}>
                    <div className={`navbar-profile-icon ${isPremium ? "premium" : "free"}`}>
                        {isPremium ? <Crown size={27} /> : <CircleUserRound size={27} />}
                    </div>

                    <div className="navbar-profile-info">
                        <h4> Welcome, {profile?.full_name || profile?.username || "Traveler"}</h4>
                        <span className={isPremium ? "premium-label" : "free-label"}>{isPremium ? "Premium Member" : "Free Member"}</span>
                    </div>
                </button>
            </div>
        </header>
    )
}