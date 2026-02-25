import { useNavigate } from "react-router-dom";
import { FileSearch } from "lucide-react";
import { Shield } from "lucide-react";
import { Users } from "lucide-react";
import { Activity } from "lucide-react";
import "./Home.css";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">

      {/* Hero Section */}
      <section className="hero">
        <h1 className="brand">
          <Activity className="brand-icon" size={28} strokeWidth={2.5} />
          <span>CirrhoX</span>
        </h1>

        <h2 className="subtitle">
          AI-Powered Liver Fibrosis & Cirrhosis Detection
        </h2>

        <p className="description">
          Leveraging machine learning to analyze clinical biomarkers and
          ultrasound imaging for early detection and staging of liver disease.
        </p>

        <div className="hero-buttons">
          <button
            className="primary-btn"
            onClick={() => navigate("/login")}
          >
            Login
          </button>

          <button
            className="secondary-btn"
            onClick={() => navigate("/register")}
          >
            Register
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">

        <div className="feature-card">
          <FileSearch className="icon" size={32} />
          <h3>Smart Analysis</h3>
          <p>
            Upload biomarkers and ultrasound for instant AI-powered
            liver assessment.
          </p>
        </div>

        <div className="feature-card">
          <Shield size={32} className="icon" />
          <h3>Clinical Accuracy</h3>
          <p>
            Trained on validated datasets for reliable fibrosis staging results.
          </p>
        </div>

        <div className="feature-card">
          <Users size={32} className="icon" />
          <h3>Role-Based Access</h3>
          <p>
            Separate dashboards for doctors and patients with full
            history tracking.
          </p>
        </div>

      </section>

      {/* Footer */}
      <footer className="footer">
        © 2025 CirrhoX. All rights reserved.
      </footer>

    </div>
  );
}