import {ArcElement, BarElement, CategoryScale, Chart as ChartJs, Legend, LinearScale, Tooltip,} from "chart.js"
import { MapPin, Plane, TrendingUp, Wallet } from "lucide-react";
import "./AnalyticsPage.css"
import {Bar, Doughnut} from "react-chartjs-2"

ChartJs.register(CategoryScale,LinearScale,BarElement,ArcElement,Tooltip,Legend)

export default function AnalyticsPage() {
    const spendingData = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [
            {
                label: "Travel Spending",
                data: [4500, 6200, 3800, 7500, 5200, 8100],
                backgroundColor: "#2563eb",
                borderRadius: 6,
            },
        ],
    }

    const expenseData = {
        labels: ["Transport", "Accommodation", "Food", "Activities"],
        datasets: [
            {
                data: [3500, 5000, 2500, 2000],
                backgroundColor: [
                    "#2563eb",
                    "#0d9488",
                    "#f59e0b",
                    "#8b5cf6",
                ],
                borderWidth: 0,
            },
        ],
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }

    const doughnutOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: "bottom" as const }
        }
    }

    return (
        <div className="analytics-page">
            <div className="analytics-heading">
                <div>
                    <h1>Travel Analytics</h1>
                    <p>Understand your travel spending and journey statistics.</p>
                </div>
            </div>

            <div className="analytics-stats">
                <div className="analytics-stat-card">
                    <div className="stat-icon blue">
                        <Wallet size={22} />
                    </div>
                    <div>
                        <span>Total Spending</span>
                        <h2>₹28,500</h2>
                    </div>
                </div>

                <div className="analytics-stat-card">
                    <div className="stat-icon green">
                        <Plane size={22} />
                    </div>
                    <div>
                        <span>Trips Completed</span>
                        <h2>8</h2>
                    </div>
                </div>

                 <div className="analytics-stat-card">
                    <div className="stat-icon orange">
                        <MapPin size={22} />
                    </div>
                    <div>
                        <span>Destinations Visited</span>
                        <h2>6</h2>
                    </div>
                </div>

                <div className="analytics-stat-card">
                    <div className="stat-icon purple">
                        <TrendingUp size={22} />
                    </div>
                    <div>
                        <span>Average Trip Cost</span>
                        <h2>₹3,562</h2>
                    </div>
                </div>
            </div>

             <div className="analytics-charts">
                <div className="analytics-chart-card">
                    <h3>Monthly Travel Spending</h3>
                    <div className="chart-container">
                        <Bar data={spendingData} options={barOptions} />
                    </div>
                </div>

                <div className="analytics-chart-card">
                    <h3>Expense Distribution</h3>
                    <div className="chart-container">
                        <Doughnut data={expenseData} options={doughnutOptions} />
                    </div>
                </div>
            </div>
        </div>
    )

}