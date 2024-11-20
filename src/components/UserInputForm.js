import React, { useState } from 'react';
import { sendFormData } from '../services/apiService'; // Axios API service

const UserInputForm = () => {
    const [medicines, setMedicines] = useState([{ name: '', stock: '', demand: '' }]);
    const [alertMessage, setAlertMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate form data
        const invalidEntries = medicines.filter(
            (medicine) => !medicine.name || medicine.stock <= 0 || medicine.demand <= 0
        );

        if (invalidEntries.length > 0) {
            setErrorMessage('Please provide valid inputs for all medicines.');
            return;
        }

        try {
            const response = await sendFormData(medicines); // Send validated data to backend
            console.log('Response from backend:', response); // Log backend response
            setAlertMessage('Data successfully sent to the backend!');
            setErrorMessage('');
        } catch (error) {
            console.error('Error sending data:', error); // Log the error for debugging
            setAlertMessage('');
            setErrorMessage('Error sending data to the backend. Please try again.');
        }
    };

    // Handle input changes
    const handleChange = (index, field, value) => {
        const updatedMedicines = [...medicines];
        updatedMedicines[index][field] = value;
        setMedicines(updatedMedicines);
    };

    // Add a new medicine input group
    const addMedicine = () => {
        setMedicines([...medicines, { name: '', stock: '', demand: '' }]);
    };

    // Remove a medicine input group
    const removeMedicine = (index) => {
        const updatedMedicines = medicines.filter((_, i) => i !== index);
        setMedicines(updatedMedicines);
    };

    return (
        <form onSubmit={handleSubmit}>
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

            <button type="button" onClick={addMedicine}>Add Medicine</button>
            <button type="submit">Submit</button>

            {alertMessage && <div className="alert-message">{alertMessage}</div>}
            {errorMessage && <div className="error-message">{errorMessage}</div>}
        </form>
    );
};

export default UserInputForm;















