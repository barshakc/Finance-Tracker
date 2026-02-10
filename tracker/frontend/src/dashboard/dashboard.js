import React, { useEffect, useState } from "react";
import { Bar, Pie, Line, Doughnut } from "react-chartjs-2";
import KPI from "./KPI";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Tooltip,
  Legend,
);

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [period, setPeriod] = useState("monthly");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await api.get("/auth/transactions/dashboard/");
        setDashboardData(res.data);
      } catch {
        setError("Failed to load dashboard");
      }
    };
    fetchDashboard();
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!dashboardData) return <p>Loading dashboard...</p>;

  const periodData = dashboardData[period];
  const kpis = dashboardData.kpis || {};

  const toNumber = (v) => Number(v) || 0;

  const expenseMap = periodData.expenses || {};
  const incomeMap = periodData.income || {};

  const labels = Object.keys(expenseMap);
  const expenseValues = Object.values(expenseMap).map(toNumber);
  const incomeValues = Object.values(incomeMap).map(toNumber);

  const totalExpenses = expenseValues.reduce((a, b) => a + b, 0);
  const totalIncome = incomeValues.reduce((a, b) => a + b, 0);
  const savings = totalIncome - totalExpenses;
  const savingsTrend = expenseValues.map((e, i) => (incomeValues[i] || 0) - e);

  const budgetArray = periodData.budget || [];
  const budgetLabels = budgetArray.map((b) => b.category);
  const budgetValues = budgetArray.map((b) => toNumber(b.limit_amount));
  const budgetUsed = toNumber(kpis.budget_used_percentage);

  const chartOptions = {
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: "#e0e0e0" } } },
    scales: {
      x: { ticks: { color: "#e0e0e0" }, grid: { color: "#333" } },
      y: { ticks: { color: "#e0e0e0" }, grid: { color: "#333" } },
    },
  };

  const expenseLineChart = {
    labels,
    datasets: [
      {
        label: "Expenses",
        data: expenseValues,
        borderColor: "#e63946",
        backgroundColor: "rgba(230,57,70,0.15)",
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const incomeExpenseTrendChart = {
    labels,
    datasets: [
      {
        label: "Income",
        data: incomeValues,
        borderColor: "#457b9d",
        tension: 0.4,
      },
      {
        label: "Expenses",
        data: expenseValues,
        borderColor: "#e63946",
        tension: 0.4,
      },
    ],
  };

  const savingsTrendChart = {
    labels,
    datasets: [
      {
        label: "Savings",
        data: savingsTrend,
        borderColor: "#2a9d8f",
        backgroundColor: "rgba(42,157,143,0.15)",
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const summaryPieChart = {
    labels: ["Income", "Expenses", "Savings"],
    datasets: [
      {
        data: [totalIncome, totalExpenses, savings],
        backgroundColor: ["#457b9d", "#e63946", "#2a9d8f"],
      },
    ],
  };

  const budgetVsExpenseChart = {
    labels: budgetLabels,
    datasets: [
      { label: "Budget", data: budgetValues, backgroundColor: "#2a9d8f" },
      {
        label: "Actual Expense",
        data: budgetLabels.map((label) => {
          const key = Object.keys(expenseMap).find(
            (k) => k.toLowerCase() === label.toLowerCase(),
          );
          return key ? expenseMap[key] : 0;
        }),
        backgroundColor: "#e63946",
      },
    ],
  };

  const budgetUtilizationChart = {
    labels: ["Used", "Remaining"],
    datasets: [
      {
        data: [budgetUsed, 100 - budgetUsed],
        backgroundColor: [budgetUsed > 90 ? "#e63946" : "#2a9d8f", "#333"],
        cutout: "70%",
      },
    ],
  };

  const container = {
    padding: "32px",
    background: "#121212",
    minHeight: "100vh",
    fontFamily: "'Inter', system-ui, sans-serif",
    color: "#e0e0e0",
  };

  const header = { maxWidth: "1400px", margin: "0 auto 32px" };
  const grid = {
    maxWidth: "1400px",
    margin: "0 auto",
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))",
    gap: "28px",
  };

  const card = {
    background: "#1e1e1e",
    borderRadius: "16px",
    padding: "22px",
    boxShadow: "0 12px 28px rgba(0,0,0,0.6)",
    border: "1px solid #2c2c2c",
    minHeight: "360px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    color: "#e0e0e0",
  };

  const kpiRow = {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "24px",
    marginBottom: "40px",
  };

  const chartWrapper = { height: "260px" };

  return (
    <div style={container}>
      <div style={header}>
        <h2
          style={{
            marginBottom: "4px",
            fontWeight: 600,
            letterSpacing: "-0.3px",
            color: "#fff",
          }}
        >
          Analytics Dashboard
        </h2>
        <p style={{ color: "#b0b0b0", marginBottom: "24px", fontSize: "14px" }}>
          Overview of your income, expenses, savings, and budget utilization
        </p>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "28px",
          }}
        >
          <button
            onClick={() => navigate("/add-data")}
            style={{
              padding: "8px 14px",
              background: "#457b9d",
              color: "#fff",
              borderRadius: "8px",
              border: "none",
              cursor: "pointer",
              fontWeight: 500,
            }}
          >
            ← Back
          </button>

          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            style={{
              padding: "10px 16px",
              borderRadius: "10px",
              border: "1px solid #444",
              background: "#1e1e1e",
              color: "#e0e0e0",
              fontWeight: 500,
            }}
          >
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>

        <div style={kpiRow}>
          <KPI title="Total Income" value={`₹ ${kpis.total_income ?? 0}`} />
          <KPI title="Total Expense" value={`₹ ${kpis.total_expense ?? 0}`} />
          <KPI title="Net Savings" value={`₹ ${kpis.net_savings ?? 0}`} />
          <KPI title="Budget Used" value={`${budgetUsed}%`} />
        </div>
      </div>

      <h3
        style={{
          maxWidth: "1400px",
          margin: "0 auto 20px",
          fontWeight: 600,
          color: "#e0e0e0",
        }}
      >
        Financial Insights
      </h3>

      <div style={grid}>
        <div style={card}>
          <h4
            style={{
              marginBottom: "12px",
              fontSize: "15px",
              fontWeight: 600,
              color: "#e0e0e0",
            }}
          >
            Expense Trend
          </h4>
          <div style={chartWrapper}>
            <Line data={expenseLineChart} options={chartOptions} />
          </div>
        </div>

        <div style={card}>
          <h4
            style={{
              marginBottom: "12px",
              fontSize: "15px",
              fontWeight: 600,
              color: "#e0e0e0",
            }}
          >
            Income vs Expense
          </h4>
          <div style={chartWrapper}>
            <Line data={incomeExpenseTrendChart} options={chartOptions} />
          </div>
        </div>

        <div style={card}>
          <h4
            style={{
              marginBottom: "12px",
              fontSize: "15px",
              fontWeight: 600,
              color: "#e0e0e0",
            }}
          >
            Savings Trend
          </h4>
          <div style={chartWrapper}>
            <Line data={savingsTrendChart} options={chartOptions} />
          </div>
        </div>

        <div style={card}>
          <h4
            style={{
              marginBottom: "12px",
              fontSize: "15px",
              fontWeight: 600,
              color: "#e0e0e0",
            }}
          >
            Income vs Expense vs Savings
          </h4>
          <div style={chartWrapper}>
            <Pie data={summaryPieChart} options={chartOptions} />
          </div>
        </div>

        <div style={card}>
          <h4
            style={{
              marginBottom: "12px",
              fontSize: "15px",
              fontWeight: 600,
              color: "#e0e0e0",
            }}
          >
            Budget vs Expenses
          </h4>
          <div style={chartWrapper}>
            <Bar data={budgetVsExpenseChart} options={chartOptions} />
          </div>
        </div>

        <div style={card}>
          <h4
            style={{
              marginBottom: "12px",
              fontSize: "15px",
              fontWeight: 600,
              color: "#e0e0e0",
            }}
          >
            Budget Utilization
          </h4>
          <div style={chartWrapper}>
            <Doughnut data={budgetUtilizationChart} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
}
