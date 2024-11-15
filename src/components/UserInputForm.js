import React, { useState } from 'react';

const UserInputForm = () => {
    // State to manage a list of medicines
    const [medicines, setMedicines] = useState([{ name: '', stock: '', demand: '' }]);
    // State to hold alert messages
    const [alertMessage, setAlertMessage] = useState('');
    
    // Handle form submission: Check for low stock and log submitted data
    const handleSubmit = (e) => {
        e.preventDefault();
        let alerts = []; // Array to collect multiple alerts

        medicines.forEach(medicine => {
            if (medicine.stock <= 20) {
                alerts.push(`Warning: Low stock for ${medicine.name}!`);
            }
        });

        // Set the alert message based on collected alerts
        if (alerts.length > 0) {
            setAlertMessage(alerts.join(' ')); // Join alerts into a single string
        } else {
            setAlertMessage(''); // Clear alert if no conditions are met
        }

        console.log('Form submitted with values:', medicines); // For demonstration purposes
    };




    // Handle input changes: Update state for a specific field of a specific medicine
    const handleChange = (index, field, value) => {
        const updatedMedicines = [...medicines];
        updatedMedicines[index][field] = value;
        setMedicines(updatedMedicines);
    };

    // Add new medicine input fields: Allow user to dynamically add more medicines
    const addMedicine = () => {
        setMedicines([...medicines, { name: '', stock: '', demand: '' }]);
    };

    // Remove a specific medicine input group
    const removeMedicine = (index) => {
        const updatedMedicines = medicines.filter((_, i) => i !== index);
        setMedicines(updatedMedicines);
    };

    return (
        <form onSubmit={handleSubmit}>
            {/* Loop through medicines array to create input fields for each medicine */}
            {medicines.map((medicine, index) => (
                <div key={index} className="medicine-input-group">
                    <label htmlFor={`medicineName-${index}`}>Medicine Name:</label>
                    <input
                        type="text"
                        id={`medicineName-${index}`}
                        value={medicine.name}
                        onChange={(e) => handleChange(index, 'name', e.target.value)}
                        required
                    />

                    <label htmlFor={`currentStock-${index}`}>Current Stock:</label>
                    <input
                        type="number"
                        id={`currentStock-${index}`}
                        value={medicine.stock}
                        onChange={(e) => handleChange(index, 'stock', e.target.value)}
                        required
                    />

                    <label htmlFor={`dailyDemand-${index}`}>Expected Daily Demand:</label>
                    <input
                        type="number"
                        id={`dailyDemand-${index}`}
                        value={medicine.demand}
                        onChange={(e) => handleChange(index, 'demand', e.target.value)}
                        required
                    />

                    {/* Button to remove a medicine input group */}
                    {medicines.length > 1 && (
                        <button
                            type="button"
                            onClick={() => removeMedicine(index)}
                            className="remove-button"
                        >
                            Remove
                        </button>
                    )}
                </div>
            ))}

            {/* Button to add new medicine input fields */}
            <button type="button" onClick={addMedicine}>Add Medicine</button>
            {/* Submit button to submit the form */}
            <button type="submit">Submit</button>

            {/* Display alert message if conditions are met */}
            {alertMessage && <div className="alert-message">{alertMessage}</div>}
        </form>
    );
};

export default UserInputForm;










