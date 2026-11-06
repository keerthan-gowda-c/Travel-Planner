import { useEffect, useState } from "react"
import "./ProfilePage.css"
import type { UserProfile } from "../../types/auth"
import { getUserProfile } from "../../services/authService";
import { isAxiosError } from "axios";
import { AtSign, Crown, Mail, ShieldCheck, User } from "lucide-react";

export default function ProfilePage() {
    const [profile, setProfile] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                setLoading(true);
                const data = await getUserProfile();
                setProfile(data)
            } catch (error: unknown) {
                if (isAxiosError(error)) {
                    setError(error.response?.data?.detail || "Unable to load your profile.")
                } else {
                    setError("Something went wrong.");
                }
            } finally {
                setLoading(false);
            }
        }
        fetchProfile()
    }, [])

    if (loading) {
        return <div className="profile-loading">Loading Profile...</div>
    }
    if (error) {
        return <div className="profile-error">{error}</div>
    }
    if (!profile) {
        return null;
    }

    const isPremium = profile.subscription.plan === "premium" && profile.subscription.status === "active";

    return (
        <div className="profile-page">
            <div className="profile-heading">
                <h1>My Profile</h1>
                <p>Manage your account information and subscription.</p>
            </div>
            <div className="profile-card">
                <div className="rpofile-avatar">
                    <User size={36} />
                </div>
                <h2>{profile.full_name || profile.username}</h2>
                <p className="profile-email">{profile.email}</p>

                <div className="profile-divider"></div>

                <div className="profile-details">
                    <div className="profile-detail-item">
                        <div className="profile-detail-icon">
                            <User size={20} />
                        </div>

                        <div>
                            <span>Full Name</span>
                            <h4>{profile.full_name || "Not Provided"}</h4>
                        </div>
                    </div>

                    <div className="profile-detail-item">
                        <div className="profile-detail-icon">
                            <AtSign size={20} />
                        </div>

                        <div>
                            <span>UserName</span>
                            <h4>{profile.username}</h4>
                        </div>
                    </div>

                    <div className="profile-detail-item">
                        <div className="profile-detail-icon">
                            <Mail size={20} />
                        </div>

                        <div>
                            <span>Email</span>
                            <h4>{profile.email}</h4>
                        </div>
                    </div>

                    <div className="profile-detail-item">
                        <div className="profile-detail-icon">
                            {isPremium ? <Crown /> : <ShieldCheck />}
                        </div>

                        <div>
                            <span>Subscription Plan</span>
                            <h4>{isPremium ? "Premium" : "Free"}
                            </h4>
                        </div>
                    </div>

                    <div className="profile-detail-item">
                        <div className="profile-detail-icon">
                            <ShieldCheck size={20} />
                        </div>

                        <div>
                            <span>Subscription Status</span>
                            <h4>{profile.subscription.status}</h4>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}