import { ChartNoAxesCombined, CreditCard, LayoutDashboard, Map, Plane } from "lucide-react"
import "./Sidebar.css"
import { NavLink } from "react-router-dom"


export default function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="sidebar-brand">
                <Plane size={25} />
                <h2>Travel Planner</h2>
            </div>

            <nav className="sidebar-nav">

                <NavLink to="/" end>
                    <LayoutDashboard size={19} /> <span>Dashboard</span>
                </NavLink>

                <NavLink to="/trips" end>
                    <Map size={19} /> <span>My Trips</span>
                </NavLink>

                <NavLink to="/analytics" end>
                    <ChartNoAxesCombined size={19} /> <span>Analytics</span>
                </NavLink>

                <NavLink to="/subscription" end>
                    <CreditCard size={19} /> <span>Subscription</span>
                </NavLink>

            </nav>
        </aside>
    )
}
