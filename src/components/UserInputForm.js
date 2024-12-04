import React, { useState } from "react";
import "../styles/StyledUserInputForm.css";

const UserInputForm = () => {
  const [medicineData, setMedicineData] = useState({
    name: "",
    stock: "",
    demand: "",
  });
  const [medicines, setMedicines] = useState([]);
  const [feedbackMessage, setFeedbackMessage] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setMedicineData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddMedicine = () => {
    if (!medicineData.name || !medicineData.stock || !medicineData.demand) {
      setFeedbackMessage("Please fill out all fields!");
      return;
    }
    if (isNaN(medicineData.stock) || isNaN(medicineData.demand)) {
      setFeedbackMessage("Stock and demand must be numeric values!");
      return;
    }
    setMedicines([...medicines, medicineData]);
    setMedicineData({ name: "", stock: "", demand: "" });
    setFeedbackMessage("Medicine added successfully!");
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/submit-data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ medicines }),
      });
      if (response.ok) {
        const data = await response.json();
        setFeedbackMessage("Data successfully sent to the backend!");
        console.log("Response from backend:", data);
      } else {
        throw new Error("Failed to send data to the backend.");
      }
    } catch (error) {
      console.error(error);
      setFeedbackMessage("Error sending data to the backend. Please try again.");
    }
  };

  return (
    <div className="main-container">
      <div className="form-container">
        <h1 className="title">Pharma Demand AI</h1>
        <p className="description">
          A tool to manage medicine stock levels and forecast demand.
        </p>
        <form>
          <div className="form-group">
            <label htmlFor="medicineName">Medicine Name</label>
            <input
              type="text"
              id="medicineName"
              name="name"
              value={medicineData.name}
              onChange={handleChange}
              className="form-control"
              placeholder="Enter medicine name"
            />
          </div>
          <div className="form-group">
            <label htmlFor="currentStock">Current Stock</label>
            <input
              type="text"
              id="currentStock"
              name="stock"
              value={medicineData.stock}
              onChange={handleChange}
              className="form-control"
              placeholder="Enter current stock"
            />
          </div>
          <div className="form-group">
            <label htmlFor="dailyDemand">Expected Daily Demand</label>
            <input
              type="text"
              id="dailyDemand"
              name="demand"
              value={medicineData.demand}
              onChange={handleChange}
              className="form-control"
              placeholder="Enter daily demand"
            />
          </div>
          <div className="button-group">
            <button
              type="button"
              onClick={handleAddMedicine}
              className="btn btn-primary"
            >
              Add Medicine
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              className="btn btn-success"
            >
              Submit
            </button>
          </div>
        </form>
        {feedbackMessage && (
          <div className="feedback-message">{feedbackMessage}</div>
        )}
      </div>
    </div>
  );
};

export default UserInputForm;
