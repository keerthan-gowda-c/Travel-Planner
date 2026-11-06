import { BrowserRouter, Route, Routes } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import TripsPage from "../pages/trips/TripsPage";
import CreateTripPage from "../pages/trips/CreateTripPage";
import TripDetailsPage from "../pages/trips/TripDetailsPage";
import AnalyticsPage from "../pages/freeUser/analytics/AnalyticsPage";
import SubscriptionPage from "../pages/subscription/SubscriptionPage";
import DashboardPage from "../pages/freeUser/dashboard/DashboardPage";
import PremiumDashboardPage from "../pages/premiumUser/dashboard/PremiumDashboardPage";
import PremiumAnalyticsPage from "../pages/premiumUser/analytics/PremiumAnalyticsPage";
import LoginPage from "../pages/auth/LoginPage";
import RegisterPage from "../pages/auth/RegisterPage";


export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Login Page and Register Page */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />


                {/* Main Layout */}
                <Route element={<MainLayout />}>
                    {/* Free Users */}
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/analytics" element={<AnalyticsPage />} />

                    {/* Premium Users */}
                    <Route path="/premium-dashboard" element={<PremiumDashboardPage />} />
                    <Route path="/premium-analytics" element={<PremiumAnalyticsPage />} />

                    <Route path="/trips" element={<TripsPage />} />
                    <Route path="/trips/create" element={<CreateTripPage />} />
                    <Route path="/trips/:tripTitle" element={<TripDetailsPage />} />

                    {/* Subscription Page */}
                    <Route path="/subscription" element={<SubscriptionPage />} />

                </Route>
                <Route path="*" element={<h1>Page Not Found</h1>} />
            </Routes>
        </BrowserRouter>
    )
}



