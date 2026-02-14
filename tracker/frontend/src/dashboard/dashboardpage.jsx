import { useState } from 'react';
import AddDataForm from './addDataform';
import Dashboard from './dashboard';
import DashboardButton from './dashboardbutton';

export default function DashboardPage() {
  const [showDashboard, setShowDashboard] = useState(false);
  const [refreshDashboard, setRefreshDashboard] = useState(false);

  const handleDataAdded = () => {
    setRefreshDashboard((prev) => !prev);
  };

  return (
    <div style={{ display: 'flex', gap: '20px', padding: '20px' }}>
      <AddDataForm onDataAdded={handleDataAdded} />

      <div style={{ flex: 1 }}>
        <DashboardButton onClick={() => setShowDashboard(true)} />

        {showDashboard && <Dashboard refresh={refreshDashboard} />}
      </div>
    </div>
  );
}
