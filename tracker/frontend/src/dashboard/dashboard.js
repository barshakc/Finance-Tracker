import { useEffect, useState } from "react";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import api from "../api/axios";
import { useNavigate } from "react-router-dom";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
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
      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard");
      }
    };
    fetchDashboard();
  }, []);

  if (error) return <p style={{ color: "red" }}>{error}</p>;
  if (!dashboardData) return <p>Loading dashboard...</p>;

  const periodData = dashboardData[period];


  const expenseLabels = Object.keys(periodData.expenses || {});
  const expenseValues = Object.values(periodData.expenses || {});

  const incomeValues = Object.values(periodData.income || {});

  const totalExpenses = expenseValues.reduce((a, b) => a + b, 0);
  const totalIncome = incomeValues.reduce((a, b) => a + b, 0);

  const budgetLabels = Object.keys(periodData.budget || {});
  const budgetValues = Object.values(periodData.budget || {});

  const hasData = totalExpenses > 0 || totalIncome > 0;

  const expensesBarChart = {
    labels: expenseLabels,
    datasets: [
      {
        label: "Expenses",
        data: expenseValues,
        backgroundColor: "#FF6384",
        borderRadius: 6,
        barThickness: 35,
      },
    ],
  };

  const expenseIncomePieChart = {
    labels: ["Expenses", "Income"],
    datasets: [
      {
        data: [totalExpenses, totalIncome],
        backgroundColor: ["#FF6384", "#36A2EB"],
        hoverOffset: 4,
      },
    ],
  };

  const budgetVsExpenseBarChart = {
    labels: budgetLabels,
    datasets: [
      {
        label: "Budget",
        data: budgetValues,
        backgroundColor: "#4BC0C0",
        borderRadius: 6,
        barThickness: 30,
      },
      {
        label: "Actual Expense",
        data: budgetLabels.map(
          (label) => periodData.expenses?.[label] || 0
        ),
        backgroundColor: "#FF6384",
        borderRadius: 6,
        barThickness: 30,
      },
    ],
  };


  const containerStyle = {
    padding: "30px",
    maxWidth: "1200px",
    margin: "0 auto",
  };

  const chartsWrapper = {
    display: "flex",
    gap: "30px",
    flexWrap: "wrap",
  };

  const chartBox = {
    flex: "1 1 45%",
    minWidth: "300px",
    height: "350px",
  };

  const selectStyle = {
    padding: "10px 15px",
    borderRadius: "8px",
    fontSize: "16px",
    marginBottom: "25px",
    cursor: "pointer",
  };

  return (
    <div style={containerStyle}>
      <h2>Analytics Dashboard</h2>

      <button
        onClick={() => navigate("/add-data")}
        style={{
          marginBottom: "20px",
          padding: "8px 16px",
          background: "#333",
          color: "#fff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        ← Back
      </button>

      <div>
        <label style={{ fontWeight: "bold", marginRight: "10px" }}>
          View:
        </label>
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value)}
          style={selectStyle}
        >
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>
      </div>

      {!hasData ? (
        <p>No data available for this period.</p>
      ) : (
        <div style={chartsWrapper}>
          {/* Monthly Expense Bar */}
          <div style={chartBox}>
            <h3>
              {period === "monthly" ? "Monthly Expenses" : "Yearly Expenses"}
            </h3>
            <Bar
              data={expensesBarChart}
              options={{ responsive: true, maintainAspectRatio: false }}
            />
          </div>

          {/* Expense vs Income Pie */}
          <div style={chartBox}>
            <h3>Expense vs Income</h3>
            <Pie
              data={expenseIncomePieChart}
              options={{ responsive: true, maintainAspectRatio: false }}
            />
          </div>

          {/* Budget vs Expense Bar */}
          {budgetLabels.length > 0 && (
            <div style={chartBox}>
              <h3>Budget vs Expense</h3>
              <Bar
                data={budgetVsExpenseBarChart}
                options={{ responsive: true, maintainAspectRatio: false }}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
