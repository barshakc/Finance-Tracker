import { useEffect, useState } from "react";
import api from "../api/axios";

export default function ExpenseChart() {
  const [data, setData] = useState({});

  useEffect(() => {
    api.get("/auth/transactions/monthly-expense/")
      .then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h2>Monthly Expenses</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}
