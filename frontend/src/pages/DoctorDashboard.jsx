import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function DoctorDashboard() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token || role !== "doctor") {
      navigate("/");
    }
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  }

  return (
    <div style={{ padding: "40px" }}>
      <h1>Doctor Dashboard</h1>
      <p>Welcome Doctor 👨‍⚕️</p>

      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button onClick={() => navigate("/history")}>
          View All Patient History
        </button>

        <button onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}