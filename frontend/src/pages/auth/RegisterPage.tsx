import { useState } from "react";
import "./Auth.css";
import { Eye, EyeOff, Lock, Mail, Plane, User } from "lucide-react";
import { Link } from "react-router-dom";
import { registerUser } from "../../services/authService";
import { isAxiosError } from "axios";

export default function RegisterPage() {
    const [fullName, setFullName] = useState("")
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false)
    const [error, setError] = useState("")

    const [loading, setLoading] = useState(false)
    const [success, setSuccess] = useState("")

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("")
        setSuccess("")

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }
        try {
            setLoading(true);
            await registerUser({
                full_name: fullName.trim(),
                username: username.trim(),
                email: email.trim(),
                password,
            })
            setSuccess("Account vreated successfully! You can now sign in.")
            setFullName("")
            setUsername("")
            setEmail("")
            setPassword("")
            setConfirmPassword("")
        }
        catch (error: unknown) {
            if (isAxiosError(error)) {
                const responseData = error.response?.data;

                if (responseData && typeof responseData === "object") {
                    const message = Object.values(responseData).flat().filter((value): value is string => typeof value === "string")
                    setError(message.join(" ") || "Registration failed. Please try again.")
                } else {
                    setError("Unable to connect to server. Please try again.")
                }
            }
            else {
                setError("Something went wrong. Please try again.")
            }
        } finally {
            setLoading(false);
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
                        <p>Explore more. Plan smarter.</p>
                    </div>

                    <div className="auth-card">
                        <div className="auth-heading">
                            <h1>Create Your Account</h1>
                            <p>Join us and start planning your next journey.</p>
                        </div>

                        <form onSubmit={handleSubmit}>
                            {error && <p className="auth-error">{error}</p>}

                            {success && <p className="auth-success">{success}</p>}
                            <div className="auth-form-group">
                                <label htmlFor="full-name">Full Name</label>
                                <div className="auth-input-wrapper">
                                    <User size={18} />
                                    <input type="text" id="full-name" placeholder="Enter your full name" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
                                </div>
                            </div>

                            <div className="auth-form-group">
                                <label htmlFor="username">Username</label>
                                <div className="auth-input-wrapper">
                                    <User size={18} />
                                    <input type="text" id="username" placeholder="Choose a username" value={username} onChange={(e) => setUsername(e.target.value)} required />
                                </div>
                            </div>

                            <div className="auth-form-group">
                                <label htmlFor="register-email">Email Address</label>
                                <div className="auth-input-wrapper">
                                    <Mail size={18} />
                                    <input type="email" id="register-email" placeholder="Enter your email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                                </div>
                            </div>

                            <div className="auth-form-group">
                                <label htmlFor="register-password">Password</label>
                                <div className="auth-input-wrapper">
                                    <Lock size={18} />
                                    <input type={showPassword ? "text" : "password"} id="register-password" placeholder="Create a password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                                    <button type="button" className="password-togle" onClick={() => setShowPassword(!showPassword)}>
                                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                                    </button>
                                </div>
                            </div>

                            <div className="auth-form-group">
                                <label htmlFor="confirm-password">Confirm Password</label>
                                <div className="auth-input-wrapper">
                                    <Lock size={18} />
                                    <input type={showConfirmPassword ? "text" : "password"} id="confirm-password" placeholder="Confirm your password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
                                    <button type="button" className="password-toggle" onClick={() => setShowConfirmPassword(!showConfirmPassword)}>
                                        {showConfirmPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                                    </button>
                                </div>
                            </div>

                            {error && (<p className="auth-error">{error}</p>)}
                            <button type="submit" className="auth-submit-button" disabled={loading}>
                                {loading? "Creating Account...":"Create Account"}
                            </button>

                        </form>

                        <div className="auth-divider">
                            <span>OR CONTINUE WITH</span>
                        </div>
                        <button type="button" className="google-auth-button">
                            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" />
                            Sign Up with Google
                        </button>
                        <p className="auth-switch"> Already have an account? <Link to="/login">Sign In</Link></p>
                    </div>

                    <p className="auth-footer"> Your journey begins with a single step.</p>
                </div>
            </div>
        )

    }