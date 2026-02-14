import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";
import { useState } from "react";
import AddDataForm from "./dashboard/addDataform";
import Dashboard from "./dashboard/dashboard";
import Login from "./auth/login";
import Signup from "./auth/signup";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  return (
    <Router>
      <Routes>
        <Route
          path="/login"
          element={
            <Login
              onLogin={(user) => {
                setUser(user);
                setIsAuthenticated(true);
              }}
            />
          }
        />

        <Route
          path="/signup"
          element={
            <Signup
              onSignup={(user) => {
                setUser(user);
                setIsAuthenticated(true);
              }}
            />
          }
        />

        <Route
          path="/add-data"
          element={
            isAuthenticated ? (
              <AddDataLayout user={user} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        <Route
          path="/dashboard"
          element={
            isAuthenticated ? (
              <Dashboard user={user} />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        <Route
          path="*"
          element={<Navigate to={isAuthenticated ? "/add-data" : "/login"} />}
        />
      </Routes>
    </Router>
  );
}

function AddDataLayout() {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <div style={styles.formContainer}>
        <AddDataForm />
      </div>
      <div style={styles.dashboardContainer}>
        <button
          style={styles.dashboardButton}
          onClick={() => navigate("/dashboard")}
        >
          📊 Analytics Dashboard
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    padding: "20px",
    minHeight: "100vh",
    backgroundColor: "#f5f5f5",
  },
  formContainer: {
    flex: 3,
  },
  dashboardContainer: {
    flex: 1,
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "center",
  },
  dashboardButton: {
    padding: "15px 25px",
    fontSize: "16px",
    borderRadius: "8px",
    border: "none",
    backgroundColor: "blue",
    color: "white",
    cursor: "pointer",
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
  },
};

export default App;
