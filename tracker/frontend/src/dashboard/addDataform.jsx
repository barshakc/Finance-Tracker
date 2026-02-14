import { useState, useEffect } from "react";
import api from "../api/axios";

const defaultCategories = [
  "Food",
  "Transport",
  "Entertainment",
  "Bills",
  "Health",
];

export default function AddDataForm({ onDataAdded }) {
  const [categories, setCategories] = useState(defaultCategories);

  const [expenseCategory, setExpenseCategory] = useState("");
  const [expenseAmount, setExpenseAmount] = useState("");
  const [incomeAmount, setIncomeAmount] = useState("");
  const [incomeSource, setIncomeSource] = useState("");
  const [budgetCategory, setBudgetCategory] = useState("");
  const [budgetAmount, setBudgetAmount] = useState("");
  const [budgetPeriod, setBudgetPeriod] = useState("MONTHLY");

  const [file, setFile] = useState(null);
  const [uploadMsg, setUploadMsg] = useState("");
  const [uploading, setUploading] = useState(false);

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
      setError(
        err.response?.data
          ? JSON.stringify(err.response.data)
          : "Failed to submit data."
      );
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      setUploadMsg("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      setUploadMsg("");

      const res = await api.post("/auth/transactions/upload/", formData);
      setUploadMsg(res.data.message || "File uploaded successfully!");
      setFile(null);
      onDataAdded && onDataAdded();
    } catch (err) {
      console.error(err.response?.data || err);
      setUploadMsg(err.response?.data?.error || "File upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h2 style={{ textAlign: "center", marginBottom: "15px" }}>Add Data</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}

      {/* Expense */}
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

      {/* Income */}
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

      {/* Budget */}
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

      <hr style={{ margin: "25px 0" }} />

      <h3 style={{ textAlign: "center", marginBottom: "10px" }}>
        Import Transactions
      </h3>

      <p style={{ textAlign: "center", color: "#666", fontSize: "14px" }}>
        Upload a CSV or Excel file to automatically analyze your finances
      </p>

      <div style={styles.uploadBox}>
        <input
          type="file"
          accept=".csv,.xls,.xlsx"
          id="fileUpload"
          style={{ display: "none" }}
          onChange={(e) => setFile(e.target.files[0])}
        />

        <label htmlFor="fileUpload" style={styles.uploadLabel}>
          📁 {file ? file.name : "Click to choose a file"}
        </label>

        <button
          type="button"
          onClick={handleFileUpload}
          disabled={uploading || !file}
          style={{
            ...styles.button,
            backgroundColor: uploading ? "#999" : "#222",
            marginTop: "10px",
          }}
        >
          {uploading ? "Uploading..." : "Upload & Analyze"}
        </button>
      </div>

      {uploadMsg && (
        <p
          style={{
            textAlign: "center",
            marginTop: "12px",
            color: uploadMsg.includes("success") ? "green" : "red",
          }}
        >
          {uploadMsg}
        </p>
      )}
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
  },
  uploadBox: {
    border: "2px dashed #ccc",
    borderRadius: "10px",
    padding: "20px",
    textAlign: "center",
    background: "#fafafa",
    transition: "0.3s",
  },
  uploadLabel: {
    display: "inline-block",
    padding: "12px 18px",
    borderRadius: "6px",
    background: "#f0f0f0",
    cursor: "pointer",
    fontSize: "14px",
    marginBottom: "10px",
  },
};
