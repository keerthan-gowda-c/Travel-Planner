
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Tooltip,
    Legend,
    Filler,
} from "chart.js";
import { Chart } from "react-google-charts";
import { Line, Bar } from "react-chartjs-2";

import {
    Wallet,
    TrendingUp,
    PiggyBank,
    MapPin,
} from "lucide-react";

import "./PremiumAnalyticsPage.css";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Tooltip,
    Legend,
    Filler
);

function PremiumAnalyticsPage() {
    const monthlySpending = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        datasets: [
            {
                label: "Monthly Spending",
                data: [4500, 6200, 3800, 7500, 5200, 8100],
                borderColor: "#2563eb",
                backgroundColor: "rgba(37, 99, 235, 0.12)",
                fill: true,
                tension: 0.4,
                pointRadius: 4,
            },
        ],
    };

    const expenseDistribution = [
        ["Expense Category", "Amount"],
        ["Accommodation", 5000],
        ["Food", 3500],
        ["Transport", 2500],
        ["Activities", 2000],
        ["Others", 1500],
    ];

    const budgetComparison = {
        labels: ["Mysuru", "Coorg", "Ooty", "Chennai"],
        datasets: [
            {
                label: "Planned Budget",
                data: [10000, 15000, 12000, 8000],
                backgroundColor: "#cbd5e1",
                borderRadius: 5,
            },
            {
                label: "Actual Spending",
                data: [8500, 13500, 14000, 6500],
                backgroundColor: "#2563eb",
                borderRadius: 5,
            },
        ],
    };

    const destinationComparison = {
        labels: ["Mysuru", "Coorg", "Ooty", "Chennai"],
        datasets: [
            {
                label: "Average Trip Cost",
                data: [8500, 13500, 14000, 6500],
                backgroundColor: [
                    "#2563eb",
                    "#8b5cf6",
                    "#06b6d4",
                    "#10b981",
                ],
                borderRadius: 6,
            },
        ],
    };

    const lineOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: (value: string | number) => `₹${value}`,
                },
            },
        },
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "bottom" as const,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: (value: string | number) => `₹${value}`,
                },
            },
        },
    };

    const destinationOptions = {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: "y" as const,
        plugins: {
            legend: {
                display: false,
            },
        },
        scales: {
            x: {
                beginAtZero: true,
                ticks: {
                    callback: (value: string | number) => `₹${value}`,
                },
            },
        },
    };

    const pieOptions = {
        is3D: true,
        backgroundColor: "transparent",
        chartArea: {
            width: "90%",
            height: "85%",
        },
        legend: {
            position: "right",
            alignment: "center",
            textStyle: {
                color: "#475569",
                fontSize: 12,
            },
        },
        pieSliceText: "none",
        tooltip: {
            text: "both",
        },
        colors: [
            "#2563eb",
            "#8b5cf6",
            "#06b6d4",
            "#f59e0b",
            "#10b981",
        ],
    };

    return (
        <div className="premium-analytics-page">
            <div className="premium-analytics-heading">
                <div>
                    <h1>Premium Analytics</h1>
                    <p>Explore your travel spending and financial insights.</p>
                </div>

                <span className="premium-badge">PREMIUM</span>
            </div>

            <div className="premium-stats-grid">
                <div className="premium-stat-card">
                    <div className="premium-stat-icon blue">
                        <Wallet size={21} />
                    </div>
                    <p>Total Spending</p>
                    <h2>₹42,500</h2>
                    <span>Across all trips</span>
                </div>

                <div className="premium-stat-card">
                    <div className="premium-stat-icon purple">
                        <TrendingUp size={21} />
                    </div>
                    <p>Daily Average</p>
                    <h2>₹2,125</h2>
                    <span>Average per travel day</span>
                </div>

                <div className="premium-stat-card">
                    <div className="premium-stat-icon green">
                        <PiggyBank size={21} />
                    </div>
                    <p>Budget Efficiency</p>
                    <h2>87%</h2>
                    <span>Budget utilization</span>
                </div>

                <div className="premium-stat-card">
                    <div className="premium-stat-icon orange">
                        <MapPin size={21} />
                    </div>
                    <p>Trips Analysed</p>
                    <h2>12</h2>
                    <span>Based on trip history</span>
                </div>
            </div>

            <div className="premium-chart-grid">
                <div className="premium-chart-card">
                    <h3>Monthly Spending Trend</h3>
                    <p>Track your spending over time.</p>
                    <div className="premium-chart-container">
                        <Line data={monthlySpending} options={lineOptions} />
                    </div>
                </div>

                <div className="premium-chart-card">
                    <h3>Expense Distribution</h3>
                    <p>Understand where your money goes.</p>

                    <div className="premium-chart-container pie-chart-container">
                        <Chart
                            chartType="PieChart"
                            data={expenseDistribution}
                            options={pieOptions}
                            width="100%"
                            height="100%"
                        />
                    </div>
                </div>

                <div className="premium-chart-card">
                    <h3>Budget vs Actual Spending</h3>
                    <p>Compare planned and actual trip expenses.</p>
                    <div className="premium-chart-container">
                        <Bar data={budgetComparison} options={barOptions} />
                    </div>
                </div>

                <div className="premium-chart-card">
                    <h3>Destination Cost Comparison</h3>
                    <p>Compare expenses across destinations.</p>
                    <div className="premium-chart-container">
                        <Bar
                            data={destinationComparison}
                            options={destinationOptions}
                        />
                    </div>
                </div>
            </div>

            <div className="premium-insights-card">
                <h3>Travel Spending Insights</h3>

                <div className="premium-insight-item">
                    <span className="insight-dot blue-dot"></span>
                    <p>Your highest spending category is Accommodation.</p>
                </div>

                <div className="premium-insight-item">
                    <span className="insight-dot green-dot"></span>
                    <p>You used 87% of your overall travel budget.</p>
                </div>

                <div className="premium-insight-item">
                    <span className="insight-dot orange-dot"></span>
                    <p>Ooty had the highest average trip cost in this sample.</p>
                </div>
            </div>
        </div>
    );
}

export default PremiumAnalyticsPage;
