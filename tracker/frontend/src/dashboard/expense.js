import { useEffect, useState } from 'react';
import api from '../api/axios';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';

import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
  Legend
);

export default function ExpenseChart() {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchExpenses = async () => {
      const res = await api.get('/auth/transactions/monthly-expense/');

      const labels = Object.keys(res.data);
      const values = Object.values(res.data);

      setChartData({
        labels,
        datasets: [
          {
            label: 'Monthly Expenses',
            data: values,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.4,
            fill: true,
            pointRadius: 4,
          },
        ],
      });
    };

    fetchExpenses();
  }, []);

  if (!chartData) return <p>Loading chart...</p>;

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      tooltip: {
        callbacks: {
          label: (ctx) => ` {ctx.parsed.y.toFixed(2)}`,
        },
      },
    },
    scales: {
      y: {
        ticks: {
          callback: (value) => ` {value}`,
        },
      },
    },
  };

  return (
    <div style={{ width: '800px' }}>
      <h2>Monthly Expense Trend </h2>
      <Line data={chartData} options={options} />
    </div>
  );
}
