import API from "../utils/api";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
        const res = await API.post("/login", {
        email: email,
        password: password
        });

        localStorage.setItem("token", res.data.access_token);

        const user = await API.get("/me");
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
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Login</button>
      </form>
    </div>
  );
}