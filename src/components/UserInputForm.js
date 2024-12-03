import React, { useState } from 'react';
import { sendFormData } from '../services/apiService'; // Axios API service

const UserInputForm = () => {
    const [medicines, setMedicines] = useState([{ name: '', stock: '', demand: '' }]); // Form data state
    const [alertMessage, setAlertMessage] = useState(''); // Success message
    const [errorMessage, setErrorMessage] = useState(''); // General error message

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await sendFormData(medicines); // Send data to backend
            console.log('Response from backend:', response);
            setAlertMessage('Data successfully sent to the backend!');
            setErrorMessage('');
        } catch (error) {
            console.error('Error sending data:', error);
            setAlertMessage('');
            setErrorMessage('Error sending data to the backend. Please try again.');
        }
    };

    // Validate individual fields
    const validateField = (field, value) => {
        if (!value || value === '') {
            return 'This field is required.';
        }
        if (field === 'stock' || field === 'demand') {
            if (isNaN(value) || value <= 0) {
                return 'Value must be a positive number.';
            }
        }
        return '';
    };

    // Handle input changes and validation
    const handleChange = (index, field, value) => {
        const updatedMedicines = [...medicines];
        updatedMedicines[index][field] = value;

        // Set custom validity messages
        const inputElement = document.getElementById(`${field}-${index}`);
        const validationMessage = validateField(field, value);
        if (inputElement) {
            inputElement.setCustomValidity(validationMessage);
            inputElement.reportValidity();
        }

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
                    {/* Medicine Name Input */}
                    <label htmlFor={`name-${index}`}>Medicine Name:</label>
                    <input
                        type="text"
                        id={`name-${index}`}
                        value={medicine.name}
                        onChange={(e) => handleChange(index, 'name', e.target.value)}
                        required
                    />

                    {/* Current Stock Input */}
                    <label htmlFor={`stock-${index}`}>Current Stock:</label>
                    <input
                        type="number"
                        id={`stock-${index}`}
                        value={medicine.stock}
                        onChange={(e) => handleChange(index, 'stock', e.target.value)}
                        required
                    />

                    {/* Daily Demand Input */}
                    <label htmlFor={`demand-${index}`}>Expected Daily Demand:</label>
                    <input
                        type="number"
                        id={`demand-${index}`}
                        value={medicine.demand}
                        onChange={(e) => handleChange(index, 'demand', e.target.value)}
                        required
                    />

                    {/* Remove Button */}
                    {medicines.length > 1 && (
                        <button type="button" onClick={() => removeMedicine(index)} className="remove-button">
                            Remove
                        </button>
                    )}
                </div>
            ))}

            <button type="button" onClick={addMedicine}>Add Medicine</button>
            <button type="submit">Submit</button>

            {/* General Messages */}
            {alertMessage && <div className="alert-message">{alertMessage}</div>}
            {errorMessage && <div className="error-message">{errorMessage}</div>}
        </form>
    );
};

export default UserInputForm;













