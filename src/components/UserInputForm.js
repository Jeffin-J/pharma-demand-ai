import React, { useState, useEffect } from "react";
import "../styles/StyledUserInputForm.css";

const UserInputForm = () => {
  const [medicineData, setMedicineData] = useState({
    name: "",
    stock: "",
    demand: "",
    threshold: "",
  });
  const [medicines, setMedicines] = useState([]);
  const [threshold, setThreshold] = useState(10); // Default critical threshold
  const [alerts, setAlerts] = useState([]);
  const [feedbackMessage, setFeedbackMessage] = useState("");

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setMedicineData((prev) => ({ ...prev, [name]: value }));
  };


  const handleAddMedicine = () => {
    if (!medicineData.name || !medicineData.stock || !medicineData.demand || !medicineData.threshold) {
        setFeedbackMessage("Please fill out all fields, including the threshold!");
        return;
    }
    if (isNaN(medicineData.stock) || isNaN(medicineData.demand) || isNaN(medicineData.threshold)) {
        setFeedbackMessage("Stock, demand, and threshold must be numeric values!");
        return;
    }
    setMedicines([...medicines, medicineData]);
    setMedicineData({ name: "", stock: "", demand: "", threshold: "" });
    setFeedbackMessage("Medicine added successfully!");
  };


  // Remove medicine from the list
  const handleRemoveMedicine = (index) => {
    const updatedMedicines = medicines.filter((_, i) => i !== index);
    setMedicines(updatedMedicines);
    setFeedbackMessage("Medicine removed successfully!");
  };

  // A* Algorithm to check stock status
  const checkStockLevels = () => {
    const newAlerts = [];
    medicines.forEach((medicine) => {
      const { name, stock, demand } = medicine;
      const stockLevel = parseInt(stock);
      const dailyDemand = parseInt(demand);

      // Calculate estimated days until stock runs out
      const daysUntilOutOfStock = stockLevel / dailyDemand;

      // Trigger alerts based on A* logic
      if (stockLevel <= threshold) {
        newAlerts.push(
          `⚠️ Critical Alert: Stock for "${name}" is critically low (below threshold: ${threshold}).`
        );
      } else if (daysUntilOutOfStock <= 3) {
        newAlerts.push(
          `⚠️ Warning: "${name}" will run out in approximately ${Math.ceil(
            daysUntilOutOfStock
          )} days.`
        );
      }
    });

    setAlerts(newAlerts);
  };

  // Submit medicines to backend
  const handleSubmit = async () => {
    if (medicines.length === 0) {
      setFeedbackMessage("No medicines to submit. Please add some first!");
      return;
    }
    try {
      const response = await fetch("http://127.0.0.1:5000/submit-data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(medicines),
      });
      if (response.ok) {
        const data = await response.json();
        setFeedbackMessage("Data successfully sent to the backend!");
        console.log("Response from backend:", data);
      } else {
        const errorData = await response.json();
        setFeedbackMessage(
          errorData.error || "Failed to send data to the backend."
        );
      }
    } catch (error) {
      setFeedbackMessage("Error sending data to the backend. Please try again.");
    }
  };

  // Trigger stock checks whenever medicines or threshold changes
  useEffect(() => {
    checkStockLevels();
  }, [medicines, threshold]);

  return (
    <div className="main-container">
      <div className="form-container">
        <h1 className="title">Pharma Demand AI</h1>
        <p className="description">
           A tool to manage medicine stock levels and forecast demand!  <br /> <br />
           Please fill out the form below to get started. Then, click <strong>Add Medicine </strong> 
          to add a medicine to the list. Once you have added all the medicines, click <strong>Submit </strong>.
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
         

          <div className="form-group">
            <label htmlFor="threshold">Critical Stock Threshold</label>
            <input
              type="number"
              id="threshold"
              name="threshold"
              value={medicineData.threshold === "" ? "" : medicineData.threshold} // Allow blank
              onChange={(e) => {
                const value = e.target.value;
                setMedicineData((prev) => ({
                  ...prev,
                  threshold: value === "" ? "" : parseInt(value), // Update threshold for this medicine
                }));
              }}
              className="form-control"
              placeholder="Enter critical stock threshold for this medicine"
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
        {medicines.length > 0 && (
          <div className="medicine-list">
            {medicines.map((medicine, index) => (
              <div key={index} className="medicine-block">
                <p>
                  <strong>{medicine.name}</strong>: Stock - {medicine.stock}, Demand -{" "}
                  {medicine.demand}
                </p>
                <button
                  className="btn btn-danger"
                  onClick={() => handleRemoveMedicine(index)}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}


        {alerts.length > 0 && (
          <div className="alerts-container">
            {alerts.map((alert, index) => (
              <p
                key={index}
                className={`alert ${
                  alert.includes("Critical Alert") ? "alert-critical" : "alert-warning"
                }`}
              >
                {alert}
              </p>
            ))}
          </div>
        )}


        {feedbackMessage && (
          <div className="feedback-message">{feedbackMessage}</div>
        )}
      </div>
    </div>
  );
};

export default UserInputForm;

