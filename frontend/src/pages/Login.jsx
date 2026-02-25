import API from "../utils/api";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
import { HeartPulse } from "lucide-react";
import { Activity } from "lucide-react";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const res = await API.post("/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      localStorage.setItem("token", res.data.access_token);

      const user = await API.get("/me", {
        headers: {
          Authorization: `Bearer ${res.data.access_token}`,
        },
      });

      localStorage.setItem("role", user.data.role);

      if (user.data.role === "doctor") {
        navigate("/history");
      } else {
        navigate("/dashboard");
      }
    } catch (err) {
      console.log(err.response?.data);
      alert("Login failed");
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        
        <div className="logo-section">
          <Activity className="logo-icon" size={28} strokeWidth={2.5} />
          <h1>CirrhoX</h1>
        </div>

        <h2>Welcome Back</h2>
        <p className="subtitle">Sign in to your account</p>

        <form onSubmit={handleLogin} className="login-form">
          <label>Email</label>
          <input
            type="email"
            // placeholder="jane@hospital.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Password</label>
          <input
            type="password"
            //placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit" className="login-btn">
            Login
          </button>
        </form>

        <p className="register-text">
          Don’t have an account?{" "}
          <span onClick={() => navigate("/register")}>
            Register
          </span>
        </p>

      </div>
    </div>
  );
}