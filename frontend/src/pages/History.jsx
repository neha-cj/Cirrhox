import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function History() {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token) {
      navigate("/");
      return;
    }

    const endpoint =
      role === "doctor" ? "/all-history" : "/my-history";

    fetch(`http://localhost:8000${endpoint}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch history");
        }
        return res.json();
      })
      .then((data) => setHistory(data))
      .catch((err) => setError(err.message));
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  }

  return (
    <div className="app">
      <h2>Prediction History</h2>
      <button onClick={handleLogout}>Logout</button>

      {error && <p className="error">{error}</p>}

      {history.length === 0 && !error && (
        <p>No history found.</p>
      )}

      {history.map((item) => (
        <div key={item.id} className="card">
          <p><strong>Prediction:</strong> {item.prediction}</p>
          <p><strong>Probability:</strong> {item.probability}</p>
          <p><strong>Date:</strong> {item.created_at}</p>
          <p><strong>Patient Name:</strong> {item.patient_name}</p>
        </div>
      ))}
    </div>
  );
}