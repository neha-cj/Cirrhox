import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../utils/api";
import "./patientDashboard.css";

export default function PatientDashboard() {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");

    fetchHistory();
  }, []);

  async function fetchHistory() {
    try {
      const res = await API.get("/my-history");
      setHistory(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  function getSeverityClass(level) {
    if (!level) return "severity low";
    if (level === "Low") return "severity low";
    if (level === "Moderate") return "severity medium";
    return "severity high";
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div className="header-row">
          <div className="title-section">
            <h1>My Health Records</h1>
            <p>Your liver analysis history</p>
          </div>

          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>

        <button
          className="new-prediction-btn"
          onClick={() => navigate("/predict")}
        >
          + New Prediction
        </button>
      </div>

      {history.map((item) => {
        const severity = item.severity;   // ✅ From backend

        return (
          <div key={item.id} className="record-card">
            <div className="card-top">
              <div>
                <p className="date">
                  {new Date(item.created_at).toLocaleDateString()}
                </p>
                <h2>{item.prediction || "Result"}</h2>
              </div>

              <span className={getSeverityClass(severity)}>
                {severity || "Unknown"}
              </span>
            </div>

            <div className="metrics">
              <div className="metric-box">
                <p>Bilirubin</p>
                <h3>{item.bilirubin ?? "-"}</h3>
              </div>

              <div className="metric-box">
                <p>Albumin</p>
                <h3>{item.albumin ?? "-"}</h3>
              </div>

              <div className="metric-box">
                <p>Protime</p>
                <h3>{item.protime ?? "-"}</h3>
              </div>

              <div className="metric-box">
                <p>AST</p>
                <h3>{item.ast ?? "-"}</h3>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}