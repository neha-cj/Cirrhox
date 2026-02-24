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
    const formData = new URLSearchParams();
    formData.append("username", email);   // IMPORTANT
    formData.append("password", password);

    const res = await API.post("/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    localStorage.setItem("token", res.data.access_token);

    // Now fetch user info
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