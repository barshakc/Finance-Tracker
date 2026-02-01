import { useState, useEffect } from 'react';
import api from '../api/axios';

export default function AddDataForm({ onDataAdded }) {
  const [categories, setCategories] = useState([]);

  const [expenseCategory, setExpenseCategory] = useState('');
  const [expenseAmount, setExpenseAmount] = useState('');
  const [incomeAmount, setIncomeAmount] = useState('');
  const [incomeSource, setIncomeSource] = useState('');
  const [budgetCategory, setBudgetCategory] = useState('');
  const [budgetAmount, setBudgetAmount] = useState('');
  const [budgetPeriod, setBudgetPeriod] = useState('MONTHLY');
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.get('/auth/categories/');
        setCategories(res.data);
      } catch (err) {
        console.error(err);
        setError('Failed to load categories.');
      }
    };

    fetchCategories();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (expenseAmount && !expenseCategory) {
      setError('Please enter a category for your expense.');
      return;
    }

    if (budgetAmount && !budgetCategory) {
      setError('Please enter a category for your budget.');
      return;
    }

    try {
      if (expenseAmount) {
        await api.post('/auth/transactions/', {
          transaction_type: 'EXPENSE',
          amount: Number(expenseAmount),
          category: expenseCategory.trim(),
          description: 'Expense added via form',
          date: new Date().toISOString(),
        });
      }

      if (incomeAmount) {
        await api.post('/auth/transactions/', {
          transaction_type: 'INCOME',
          amount: Number(incomeAmount),
          description: incomeSource || 'Income added via form',
          date: new Date().toISOString(),
        });
      }

      if (budgetAmount) {
        await api.post('/auth/budgets/', {
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

      setSuccess('Data added successfully!');
      onDataAdded && onDataAdded();
      setExpenseAmount('');
      setExpenseCategory('');
      setIncomeAmount('');
      setIncomeSource('');
      setBudgetAmount('');
      setBudgetCategory('');
    } catch (err) {
      console.error(err.response?.data || err);
      if (err.response?.data) {
        setError(JSON.stringify(err.response.data));
      } else {
        setError('Failed to submit data.');
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h2>Add Financial Data</h2>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}

      <h3>Expense</h3>
      <input
        style={styles.input}
        placeholder="Category (type or select)"
        list="expense-categories"
        value={expenseCategory}
        onChange={(e) => setExpenseCategory(e.target.value)}
      />
      <datalist id="expense-categories">
        {categories.map((cat) => (
          <option key={cat.id} value={cat.name} />
        ))}
      </datalist>

      <input
        style={styles.input}
        type="number"
        placeholder="Expense amount"
        value={expenseAmount}
        onChange={(e) => setExpenseAmount(e.target.value)}
      />

      <h3>Income</h3>
      <input
        style={styles.input}
        placeholder="Income source"
        value={incomeSource}
        onChange={(e) => setIncomeSource(e.target.value)}
      />
      <input
        style={styles.input}
        type="number"
        placeholder="Income amount"
        value={incomeAmount}
        onChange={(e) => setIncomeAmount(e.target.value)}
      />

      <h3>Budget</h3>
      <input
        style={styles.input}
        placeholder="Category (type or select)"
        list="budget-categories"
        value={budgetCategory}
        onChange={(e) => setBudgetCategory(e.target.value)}
      />
      <datalist id="budget-categories">
        {categories.map((cat) => (
          <option key={cat.id} value={cat.name} />
        ))}
      </datalist>

      <input
        style={styles.input}
        type="number"
        placeholder="Budget amount"
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
        <option value="WEEKLY">Weekly</option>
      </select>

      <button style={styles.button} type="submit">
        Submit
      </button>
    </form>
  );
}

const styles = {
  form: {
    maxWidth: '500px',
    margin: '50px auto',
    padding: '30px',
    background: '#fff',
    borderRadius: '8px',
    boxShadow: '0px 4px 10px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
  },
  input: {
    marginBottom: '15px',
    padding: '10px',
    borderRadius: '5px',
    border: '1px solid #ccc',
    fontSize: '16px',
  },
  button: {
    padding: '10px',
    borderRadius: '5px',
    border: 'none',
    backgroundColor: 'blue',
    color: 'white',
    fontSize: '16px',
    cursor: 'pointer',
  },
};