import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Patient + Doctor Dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={["patient", "doctor"]}>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Patient sees own history, Doctor sees all */}
        <Route
          path="/history"
          element={
            <ProtectedRoute allowedRoles={["patient", "doctor"]}>
              <History />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;