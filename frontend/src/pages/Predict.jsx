import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../utils/api";
import "./predict.css";
import { FlaskConical, Upload, CheckCircle } from "lucide-react";

export default function Predict() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) navigate("/");
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("token");

      const formData = new FormData();

      formData.append("bilirubin", e.target.bilirubin.value);
      formData.append("albumin", e.target.albumin.value);
      formData.append("protime", e.target.protime.value);
      formData.append("ast", e.target.ast.value);
      formData.append("file", e.target.file.files[0]);

      await fetch("http://localhost:8000/predict/hybrid", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      navigate("/patient"); // go back to dashboard after prediction

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
        <FlaskConical
            size={28}
            strokeWidth={2.5}
            className="predict-icon"
        />
        Liver Fibrosis Prediction
      </h1>
      <p>
        Enter clinical biomarkers and upload ultrasound for analysis
      </p>
    </div>

    <form className="predict-card" onSubmit={handleSubmit}>

      <div className="predict-grid">

        <div className="input-group">
          <label>Bilirubin (mg/dL)</label>
          <input
            name="bilirubin"
            type="number"
            step="0.01"
            placeholder="e.g. 1.2"
            required
          />
        </div>

        <div className="input-group">
          <label>Albumin (g/dL)</label>
          <input
            name="albumin"
            type="number"
            step="0.01"
            placeholder="e.g. 3.8"
            required
          />
        </div>

        <div className="input-group">
          <label>Protime (sec)</label>
          <input
            name="protime"
            type="number"
            step="0.1"
            placeholder="e.g. 12.5"
            required
          />
        </div>

        <div className="input-group">
          <label>AST (U/L)</label>
          <input
            name="ast"
            type="number"
            step="1"
            placeholder="e.g. 45"
            required
          />
        </div>

      </div>

      <div className="upload-section">
        <label>Ultrasound Image</label>

        {/* Hidden File Input */}
        <input
          type="file"
          accept="image/*"
          onChange={(e) => {
            const file = e.target.files[0];
            setSelectedFile(file);
          }}
          hidden
          id="fileUpload"
        />

        {/* Clickable Upload Box */}
        <label htmlFor="fileUpload" className="upload-box">
          {selectedFile ? (
            <div className="file-selected">
              <CheckCircle size={22} className="check-icon" />
              <span className="file-name">{selectedFile.name}</span>
            </div>
          ) : (
            <>
              <Upload size={40} strokeWidth={2} className="upload-icon" />
              <p>Click to upload ultrasound image</p>
              <span>PNG, JPG up to 10MB</span>
            </>
          )}
        </label>
      </div>

      <button
        type="submit"
        className="predict-btn"
        disabled={loading}
      >
        {loading ? "Running..." : "Run Prediction"}
      </button>

      {error && <p className="error">{error}</p>}

    </form>
  </div>
);
}