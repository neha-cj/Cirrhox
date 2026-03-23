import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./predict.css";
import { FlaskConical, Upload, CheckCircle } from "lucide-react";

export default function Predict() {
  const navigate = useNavigate();
  const { patientId } = useParams();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token) {
      navigate("/");
      return;
    }

    if (role === "doctor" && !patientId) {
      navigate("/doctor/patients");
    }
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!selectedFile) {
      setError("Please upload an ultrasound image.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("token");

      const formData = new FormData();

      if (patientId) {
        formData.append("patient_id", patientId);
      }

      formData.append("bilirubin", e.target.bilirubin.value);
      formData.append("albumin", e.target.albumin.value);
      formData.append("ast", e.target.ast.value);
      formData.append("alt", e.target.alt.value);
      formData.append("alp", e.target.alp.value);
      formData.append("file", selectedFile);

      const res = await fetch("http://localhost:8000/predict/hybrid", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Prediction failed");
      }

      // ✅ GET RESULT
      const data = await res.json();

      // ✅ SHOW POPUP INSTEAD OF NAVIGATE
      setResult(data);
      setShowPopup(true);

    } catch (err) {
      setError("Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="predict-page">

      <div className="predict-header">
        <h1 className="predict-title">
          <FlaskConical size={28} strokeWidth={2.5} className="predict-icon" />
          Liver Fibrosis Prediction
        </h1>
        <p>Enter clinical biomarkers and upload ultrasound for analysis</p>
      </div>

      <form className="predict-card" onSubmit={handleSubmit}>

        <div className="predict-grid">

          <div className="input-group">
            <label>Bilirubin (mg/dL)</label>
            <input name="bilirubin" type="number" step="0.01" required />
          </div>

          <div className="input-group">
            <label>Albumin (g/dL)</label>
            <input name="albumin" type="number" step="0.01" required />
          </div>

          <div className="input-group">
            <label>AST (U/L)</label>
            <input name="ast" type="number" required />
          </div>

          <div className="input-group">
            <label>ALT (U/L)</label>
            <input name="alt" type="number" required />
          </div>

          <div className="input-group">
            <label>ALP (U/L)</label>
            <input name="alp" type="number" required />
          </div>

        </div>

        <div className="upload-section">
          <label>Ultrasound Image</label>

          <input
            type="file"
            accept="image/*"
            onChange={(e) => setSelectedFile(e.target.files[0])}
            hidden
            id="fileUpload"
          />

          <label htmlFor="fileUpload" className="upload-box">
            {selectedFile ? (
              <div className="file-selected">
                <CheckCircle size={22} className="check-icon" />
                <span>{selectedFile.name}</span>
              </div>
            ) : (
              <>
                <Upload size={40} className="upload-icon" />
                <p>Click to upload ultrasound image</p>
              </>
            )}
          </label>
        </div>

        <button
          type="submit"
          className="predict-btn"
          disabled={loading || !selectedFile}
        >
          {loading ? "Running..." : "Run Prediction"}
        </button>

        {error && <p className="error">{error}</p>}
      </form>

      {/* ✅ POPUP */}
      {showPopup && result && (
        <div className="overlay">
          <div className="popup">

            {/* Header */}
            <h2 className="popup-title">Prediction Result</h2>

            {/* Subheading */}
            <p className="popup-subtitle">
              Liver fibrosis analysis complete
            </p>

            {/* Result Box */}
            <div className={`result-box ${result.severity?.toLowerCase()}`}>
              
              <p><strong>Diagnosis:</strong> {result.prediction}</p>
              <p><strong>Severity:</strong> {result.severity}</p>

            </div>

            {/* Button */}
            <button
              className="dashboard-btn"
              onClick={() => {
                const role = localStorage.getItem("role");

                if (role === "doctor") {
                  navigate("/doctor");
                } else {
                  navigate("/patient");
                }
              }}
            >
              Go to Dashboard
            </button>

          </div>
        </div>
      )}

    </div>
  );
}