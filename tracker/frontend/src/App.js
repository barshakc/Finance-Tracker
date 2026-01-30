import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './auth/login';
import Signup from './auth/signup';
import ExpenseChart from './dashboard/expense';

function App() {
  const isLoggedIn = !!localStorage.getItem('access');

  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={isLoggedIn ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/signup" element={isLoggedIn ? <Navigate to="/dashboard" /> : <Signup />} />

        <Route
          path="/dashboard"
          element={isLoggedIn ? <ExpenseChart /> : <Navigate to="/login" />}
        />

        <Route
          path="*"
          element={<Navigate to={isLoggedIn ? "/dashboard" : "/login"} />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
