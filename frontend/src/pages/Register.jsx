import { useState } from "react";
import API from "../utils/api";
import { useNavigate } from "react-router-dom";

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
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Name"
          onChange={(e) => setForm({...form, name: e.target.value})} />

        <input placeholder="Email"
          onChange={(e) => setForm({...form, email: e.target.value})} />

        <input type="password" placeholder="Password"
          onChange={(e) => setForm({...form, password: e.target.value})} />

        <select
          onChange={(e) => setForm({...form, role: e.target.value})}>
          <option value="patient">Patient</option>
          <option value="doctor">Doctor</option>
        </select>

        <button type="submit">Register</button>
      </form>
    </div>
  );
}