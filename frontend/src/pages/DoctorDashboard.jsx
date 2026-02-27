import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./doctorDashboard.css";

export default function DoctorDashboard() {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [sortField, setSortField] = useState("date");
  const [sortOrder, setSortOrder] = useState("desc");

  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token || role !== "doctor") {
      navigate("/");
      return;
    }

    fetchHistory();
  }, [navigate]);

  async function fetchHistory() {
    try {
      const token = localStorage.getItem("token");

      const response = await axios.get(
        "http://127.0.0.1:8000/all-history",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setHistory(response.data);
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  }

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  }

  // 🔥 Sorting Logic
  const sortedHistory = [...history].sort((a, b) => {
    let valueA, valueB;

    if (sortField === "date") {
      valueA = new Date(a.created_at);
      valueB = new Date(b.created_at);
    }

    if (sortField === "name") {
      valueA = a.patient_name?.toLowerCase();
      valueB = b.patient_name?.toLowerCase();
    }

    if (sortField === "severity") {
      const order = { Low: 1, Moderate: 2, High: 3 };
      valueA = order[a.severity] || 0;
      valueB = order[b.severity] || 0;
    }

    if (sortOrder === "asc") {
      return valueA > valueB ? 1 : -1;
    } else {
      return valueA < valueB ? 1 : -1;
    }
  });

  // Stats
  const totalRecords = history.length;
  const highRisk = history.filter((item) => item.severity === "High").length;
  const moderateRisk = history.filter((item) => item.severity === "Moderate").length;
  const lowRisk = history.filter((item) => item.severity === "Low").length;

  return (
    <div className="doctor-container">
      {/* Header */}
      <div className="doctor-header">
        <div>
          <h1>Doctor Dashboard</h1>
          <p>Patient history and analysis results</p>
        </div>

        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {/* Action */}
      <div className="action-section">
        <button
          className="primary-btn"
          onClick={() => navigate("/predict")}
        >
          + New Prediction
        </button>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Records</h3>
          <p className="stat-number">{totalRecords}</p>
        </div>

        <div className="stat-card">
          <h3>High Risk</h3>
          <p className="stat-number critical">{highRisk}</p>
        </div>

        <div className="stat-card">
          <h3>Moderate Risk</h3>
          <p className="stat-number">{moderateRisk}</p>
        </div>

        <div className="stat-card">
          <h3>Low Risk</h3>
          <p className="stat-number normal">{lowRisk}</p>
        </div>
      </div>

      {/* 🔥 Sort Controls */}
      <div className="sort-controls">
        <select
          value={sortField}
          onChange={(e) => setSortField(e.target.value)}
          className="sort-select"
        >
          <option value="date">Date</option>
          <option value="name">Name</option>
          <option value="severity">Severity</option>
        </select>

        <button
          className="sort-toggle"
          onClick={() =>
            setSortOrder(sortOrder === "asc" ? "desc" : "asc")
          }
        >
          {sortOrder === "asc" ? "↑" : "↓"}
        </button>
      </div>

      {/* Table */}
      <div className="table-section">
        <table>
          <thead>
            <tr>
              <th>Patient</th>
              <th>Date</th>
              <th>Bilirubin</th>
              <th>Albumin</th>
              <th>Protime</th>
              <th>AST</th>
              <th>Result</th>
              <th>Severity</th>
            </tr>
          </thead>
          <tbody>
            {sortedHistory.map((item) => (
              <tr key={item.id}>
                <td>{item.patient_name}</td>
                <td>{new Date(item.created_at).toLocaleDateString()}</td>
                <td>{item.bilirubin}</td>
                <td>{item.albumin}</td>
                <td>{item.protime}</td>
                <td>{item.ast}</td>
                <td>{item.prediction}</td>
                <td>
                  <span className={`badge ${item.severity?.toLowerCase()}`}>
                    {item.severity || "Unknown"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}