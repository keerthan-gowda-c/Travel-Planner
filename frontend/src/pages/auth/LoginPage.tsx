import { useState } from "react";
import "./Auth.css";
import { Eye, EyeOff, Lock, Mail, Plane } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../../services/authService";
import { isAxiosError } from "axios";

export default function LoginPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");

        try {
            setLoading(true);
            const response = await loginUser({ email: email.trim(), password: password })
            localStorage.setItem("access_token", response.access);
            localStorage.setItem("refresh_token", response.refresh);
            navigate("/dashboard")
        } catch (error: unknown) {
            if (isAxiosError(error)){
                const responseData = error.response?.data;

                if (responseData && typeof responseData === "object"){
                    const messages = Object.values(responseData).flat().filter((value): value is string => typeof value === "string")
                    setError(messages.join(" ") || "Invalid email or password.") 
                } else {
                    setError("Unable to connect to the server. Please try again.");
                }
            }
            else{
                setError("Something went wrong. Please try again.");
            }

        } finally{
            setLoading(false)
        }
    }
        return (
            <div className="auth-page">
                <div className="auth-container">
                    <div className="auth-brand">
                        <div className="auth-logo">
                            <Plane size={25} />
                        </div>
                        <h2>Travel Planner</h2>
                        <p>Explore more. Plan Smarter.</p>
                    </div>

                    <div className="auth-card">
                        <div className="auth-heading">
                            <h1>Welcome Back</h1>
                            <p>Sign in to Continue planning your journey.</p>
                        </div>

                        <form onSubmit={handleSubmit}>
                            {error && <p className="auth-error">{error}</p>}
                            <div className="auth-form-group">
                                <label htmlFor="email">Email Address</label>
                                <div className="auth-input-wrapper">
                                    <Mail size={18} />
                                    <input type="email" id="email" placeholder="Enter your email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                </div>
                            </div>

                            <div className="auth-form-group">
                                <label htmlFor="password">Password</label>
                                <div className="auth-input-wrapper">
                                    <Lock size={18} />
                                    <input type={showPassword ? "text" : "password"} id="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                                    <button type="button" className="password-toggle" onClick={() => setShowPassword(!showPassword)}>
                                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                                    </button>
                                </div>
                            </div>

                            <div className="auth-options">
                                <label className="remember-option">
                                    <input type="checkbox" />
                                    Remember me
                                </label>

                                <Link to="/forgot-password">
                                    Forgot Password?
                                </Link>
                            </div>

                            <button type="submit" className="auth-submit-button" disabled={loading}>
                                {loading?"Signing In...":"Sign In"}
                            </button>
                        </form>

                        <div className="auth-divider">
                            <span>OR CONTINUE WITH</span>
                        </div>

                        <button type="button" className="google-auth-button">
                            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" />
                            Continue with Google
                        </button>

                        <p className="auth-switch">Don't have an account <Link to="/register">Sign Up</Link></p>
                    </div>

                    <p className="auth-footer">Your journey begins with a single step.</p>
                </div>
            </div>
        )
    }