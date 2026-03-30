import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./doctorPatients.css";

export default function DoctorPatients() {

  const navigate = useNavigate();

  const [patients, setPatients] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {

    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    if (!token || role !== "doctor") {
      navigate("/");
      return;
    }

    fetchPatients();

  }, [navigate]);


  async function fetchPatients() {
    try {

      const token = localStorage.getItem("token");

      const res = await axios.get(
        "http://127.0.0.1:8000/patients",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setPatients(res.data);

    } catch (err) {
      console.error("Error fetching patients:", err);
    }
  }


  function handlePredict(patientId) {
    navigate(`/doctor/predict/${patientId}`);
  }


  const filteredPatients = patients.filter((p) =>
    p.name.toLowerCase().includes(searchTerm.toLowerCase())
  );


  return (
    <div className="doctor-patients-container">

      <div className="patients-header">
        <h1>Select Patient</h1>
        <p>Choose a patient to run liver fibrosis prediction</p>
      </div>

      <div className="patients-controls">

        <input
          type="text"
          placeholder="Search patients..."
          className="patients-search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

      </div>


      <div className="patients-table">

        <table>

          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>

            {filteredPatients.map((patient) => (

              <tr key={patient.id}>

                <td>{patient.name}</td>

                <td>{patient.email}</td>

                <td>
                  <button
                    className="predict-btn"
                    onClick={() => handlePredict(patient.id)}
                  >
                    Predict
                  </button>
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}
