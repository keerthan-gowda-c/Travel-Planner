import { Check, Crown, Plane, Sparkles } from "lucide-react";
import "./SubscriptionPage.css";

export default function SubscriptionPage() {
    return (
        <div className="subscription-page">
            <div className="subscription-heading">
                <h1>Choose your Travel Plan</h1>
                <p>Get more from your journeys with the right subscription.</p>
            </div>

            <div className="subscription-plans">
                {/* Free Plan */}
                <div className="plan-card">
                    <div className="plan-icon free-icon">
                        <Plane size={24} />
                    </div>
                    <h2>Free Plan</h2>
                    <p className="plan-description">Perfect for getting started with travel planning</p>

                    <div className="plan-price">
                        <h3>₹0</h3>
                        <span>Forever</span>
                    </div>
                    <ul className="plan-features">
                        <li><Check size={17} /> 3 free trips</li>
                        <li><Check size={17} /> One active trip at a time</li>
                        <li><Check size={17} /> Maximum 3 days per trip</li>
                        <li><Check size={17} /> Basic trip planning</li>
                        <li><Check size={17} /> Basic analytics</li>
                    </ul>

                    <button className="free-plan-button" disabled>
                        Current Free Plan
                    </button>
                </div>

                {/* Premium Plan */}
                <div className="plan-card premium-plan">
                    <div className="popular-label">Recommended</div>

                    <div className="plan-icon premium-icon">
                        <Crown size={24} />
                    </div>

                    <h2>Premium Plan</h2>
                    <p className="plan-description"> Enjoy unlimited travel planning and advanced insights.</p>

                    <div className="plan-price">
                        <h3>₹199</h3>
                        <span>/ month</span>
                    </div>

                    <ul className="plan-features">
                        <li><Check size={17} /> Unlimited trips</li>
                        <li><Check size={17} /> Multiple active trips</li>
                        <li><Check size={17} /> No trip duration restriction</li>
                        <li><Check size={17} /> Advanced analytics</li>
                        <li><Check size={17} /> Budget and spending insights</li>
                        <li><Check size={17} /> Premium dashboard themes</li>
                    </ul>

                    <button className="premium-plan-button">
                        <Sparkles size={17} />
                        Upgrade to Premium
                    </button>
                </div>
            </div>

            <p className="subscription-note">
                Premium weekly plan: ₹99. All payments will be processed securely.
            </p>

        </div>
    )
}