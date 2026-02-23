import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <h1>Welcome to Cirrhox</h1>
      <p>AI-Based Liver Fibrosis Detection System</p>

      <div className="buttons">
        <button onClick={() => navigate("/login")}>
          Login
        </button>

        <button onClick={() => navigate("/register")}>
          Register
        </button>
      </div>
    </div>
  );
}