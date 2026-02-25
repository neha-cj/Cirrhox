import { useState } from "react";
import API from "../utils/api";
import { useNavigate } from "react-router-dom";
import { Activity } from "lucide-react";
import "./Register.css";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "patient"
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await API.post("/register", form);
      alert("Registered successfully!");
      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.detail || "Error");
    }
  };

  return (
    <div className="auth-container">

      {/* Brand */}
      <div className="register-container">
        <div className="register-header">
          <h1 className="register-brand">
            <Activity className="register-brand-icon" size={28} />
            CirrhoX
          </h1>
          <h2>Create Account</h2>
          <p>Register to get started</p>
        </div>

      {/* Card */}
      <form className="register-card" onSubmit={handleSubmit}>

        <label>Full Name</label>
        <input
          //placeholder="Dr. Jane Smith"
          value={form.name}
          onChange={(e) =>
            setForm({ ...form, name: e.target.value })
          }
          required
        />

        <label>Email</label>
        <input
          type="email"
          // placeholder="jane@hospital.com"
          value={form.email}
          onChange={(e) =>
            setForm({ ...form, email: e.target.value })
          }
          required
        />

        <label>Password</label>
        <input
          type="password"
          //placeholder="••••••••"
          value={form.password}
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
          required
        />

        <label>Role</label>

        <div className="role-toggle">
          <button
            type="button"
            className={form.role === "patient" ? "active" : ""}
            onClick={() =>
              setForm({ ...form, role: "patient" })
            }
          >
            Patient
          </button>

          <button
            type="button"
            className={form.role === "doctor" ? "active" : ""}
            onClick={() =>
              setForm({ ...form, role: "doctor" })
            }
          >
            Doctor
          </button>
        </div>

        <button type="submit" className="register-btn">
          Register
        </button>

        <p className="register-footer">
          Already have an account?{" "}
          <span onClick={() => navigate("/login")}>
            Login
          </span>
        </p>
      </form>
    </div>
  </div>
  );
}