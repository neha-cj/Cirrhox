import { useState } from "react";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const formData = new FormData();

      const bilirubin = e.target.bilirubin.value;
      const albumin = e.target.albumin.value;
      const protime = e.target.protime.value;
      const ast = e.target.ast.value;
      const file = e.target.file.files[0];

      // Put clinical data as JSON string
      formData.append(
        "clinicalData",
        JSON.stringify({ bilirubin, albumin, protime, ast })
      );
      // File field (must match backend name)
      if (file) formData.append("file", file);

      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Liver Fibrosis Hybrid Prediction</h1>
        <p>Enter clinical values and upload an image to get risk prediction.</p>
      </header>

      <main className="content">
        <form className="card form-card" onSubmit={handleSubmit}>
          <h2>Input Details</h2>

          <div className="grid">
            <div className="field">
              <label>Bilirubin</label>
              <input
                name="bilirubin"
                type="number"
                step="0.01"
                placeholder="e.g. 1.2"
                required
              />
            </div>

            <div className="field">
              <label>Albumin</label>
              <input
                name="albumin"
                type="number"
                step="0.01"
                placeholder="e.g. 3.8"
                required
              />
            </div>

            <div className="field">
              <label>Protime</label>
              <input
                name="protime"
                type="number"
                step="0.1"
                placeholder="e.g. 12.5"
                required
              />
            </div>

            <div className="field">
              <label>AST</label>
              <input
                name="ast"
                type="number"
                step="1"
                placeholder="e.g. 45"
                required
              />
            </div>
          </div>

          <div className="field">
            <label>Ultrasound / CT Image</label>
            <input name="file" type="file" accept="image/*" required />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? "Predicting..." : "Predict"}
          </button>

          {error && <p className="error">{error}</p>}
        </form>

        <section className="card result-card">
          <h2>Result</h2>
          {!result && <p>No prediction yet. Submit the form to see results.</p>}
          {result && (
            <div className="result-box">
              <p>
                <strong>Final Label:</strong> {result.label || "N/A"}
              </p>
              <p>
                <strong>Final Score:</strong>{" "}
                {result.final !== undefined
                  ? result.final.toFixed(3)
                  : "N/A"}
              </p>
              <div className="probabilities">
                <p>
                  <strong>Clinical Model:</strong>{" "}
                  {result.clinical !== undefined
                    ? result.clinical.toFixed(3)
                    : "N/A"}
                </p>
                <p>
                  <strong>Image Model:</strong>{" "}
                  {result.ultrasound !== undefined
                    ? result.ultrasound.toFixed(3)
                    : "N/A"}
                </p>
              </div>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
