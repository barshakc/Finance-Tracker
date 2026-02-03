import { useState, useEffect } from "react";
import api from "../api/axios";

const defaultCategories = ["Food", "Transport", "Entertainment", "Bills", "Health"];

export default function AddDataForm({ onDataAdded }) {
  const [categories, setCategories] = useState(defaultCategories);

  const [expenseCategory, setExpenseCategory] = useState("");
  const [expenseAmount, setExpenseAmount] = useState("");
  const [incomeAmount, setIncomeAmount] = useState("");
  const [incomeSource, setIncomeSource] = useState("");
  const [budgetCategory, setBudgetCategory] = useState("");
  const [budgetAmount, setBudgetAmount] = useState("");
  const [budgetPeriod, setBudgetPeriod] = useState("MONTHLY");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.get("/auth/categories/");
        if (res.data && res.data.length > 0) {
          const merged = Array.from(
            new Set([...defaultCategories, ...res.data.map((c) => c.name)])
          );
          setCategories(merged);
        }
      } catch (err) {
        console.error("Failed to load categories", err);
        setCategories(defaultCategories);
      }
    };
    fetchCategories();
  }, []); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (expenseAmount && !expenseCategory) {
      setError("Please enter a category for your expense.");
      return;
    }
    if (budgetAmount && !budgetCategory) {
      setError("Please enter a category for your budget.");
      return;
    }

    try {
      if (expenseAmount) {
        await api.post("/auth/transactions/", {
          transaction_type: "EXPENSE",
          amount: Number(expenseAmount),
          category: expenseCategory.trim(),
          description: "Expense added via form",
          date: new Date().toISOString(),
        });
      }

      if (incomeAmount) {
        await api.post("/auth/transactions/", {
          transaction_type: "INCOME",
          amount: Number(incomeAmount),
          description: incomeSource || "Income added via form",
          date: new Date().toISOString(),
        });
      }

      if (budgetAmount) {
        await api.post("/auth/budgets/", {
          category: budgetCategory.trim(),
          limit_amount: Number(budgetAmount),
          period: budgetPeriod,
          start_date: new Date().toISOString().slice(0, 10),
          end_date: new Date(new Date().setMonth(new Date().getMonth() + 1))
            .toISOString()
            .slice(0, 10),
          is_active: true,
        });
      }

      setSuccess("Data added successfully!");
      onDataAdded && onDataAdded();

      setExpenseAmount("");
      setExpenseCategory("");
      setIncomeAmount("");
      setIncomeSource("");
      setBudgetAmount("");
      setBudgetCategory("");
    } catch (err) {
      console.error(err.response?.data || err);
      setError(err.response?.data ? JSON.stringify(err.response.data) : "Failed to submit data.");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h2 style={{ textAlign: "center", marginBottom: "15px" }}>Add Data</h2>

      {error && <p style={{ color: "red", marginBottom: "10px" }}>{error}</p>}
      {success && <p style={{ color: "green", marginBottom: "10px" }}>{success}</p>}

      <div style={styles.row}>
        <input
          style={styles.input}
          placeholder="Expense Category"
          list="expense-categories"
          value={expenseCategory}
          onChange={(e) => setExpenseCategory(e.target.value)}
        />
        <datalist id="expense-categories">
          {categories.map((cat, idx) => (
            <option key={idx} value={cat} />
          ))}
        </datalist>

        <input
          style={styles.input}
          type="number"
          placeholder="Amount"
          value={expenseAmount}
          onChange={(e) => setExpenseAmount(e.target.value)}
        />
      </div>

      <div style={styles.row}>
        <input
          style={styles.input}
          placeholder="Income Source"
          value={incomeSource}
          onChange={(e) => setIncomeSource(e.target.value)}
        />
        <input
          style={styles.input}
          type="number"
          placeholder="Amount"
          value={incomeAmount}
          onChange={(e) => setIncomeAmount(e.target.value)}
        />
      </div>

      <div style={styles.row}>
        <input
          style={styles.input}
          placeholder="Budget Category"
          list="budget-categories"
          value={budgetCategory}
          onChange={(e) => setBudgetCategory(e.target.value)}
        />
        <datalist id="budget-categories">
          {categories.map((cat, idx) => (
            <option key={idx} value={cat} />
          ))}
        </datalist>

        <input
          style={styles.input}
          type="number"
          placeholder="Amount"
          value={budgetAmount}
          onChange={(e) => setBudgetAmount(e.target.value)}
        />

        <select
          style={styles.input}
          value={budgetPeriod}
          onChange={(e) => setBudgetPeriod(e.target.value)}
        >
          <option value="MONTHLY">Monthly</option>
          <option value="YEARLY">Yearly</option>
        </select>
      </div>

      <button style={styles.button} type="submit">
        Submit
      </button>
    </form>
  );
}

const styles = {
  form: {
    maxWidth: "700px",
    margin: "30px auto",
    padding: "20px",
    background: "#fff",
    borderRadius: "8px",
    boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
  },
  row: {
    display: "flex",
    gap: "10px",
    flexWrap: "wrap",
  },
  input: {
    flex: 1,
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    fontSize: "14px",
  },
  button: {
    padding: "10px",
    borderRadius: "5px",
    border: "none",
    backgroundColor: "blue",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
    marginTop: "10px",
  },
};
