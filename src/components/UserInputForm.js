import React, { useState } from 'react';

const UserInputForm = () => {
    // State to hold form inputs
    const [medicineName, setMedicineName] = useState('');
    const [currentStock, setCurrentStock] = useState('');
    const [dailyDemand, setDailyDemand] = useState('');
    const [selectedOptions, setSelectedOptions] = useState({}); // State to track user selections

    // Handle form submission
    const handleSubmit = (e) => {
        e.preventDefault();
        // Track user selections
        const userSelections = {
            medicineName,
            currentStock,
            dailyDemand,
        };
        setSelectedOptions(userSelections); // Save user selections to state

        // Log the selected options to the console
        console.log('User Selections:', userSelections);
    };

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="medicineName">Medicine Name:</label>
            <input
                type="text"
                id="medicineName"
                name="medicineName"
                value={medicineName}
                onChange={(e) => setMedicineName(e.target.value)}
                required
            />

            <label htmlFor="currentStock">Current Stock:</label>
            <input
                type="number"
                id="currentStock"
                name="currentStock"
                value={currentStock}
                onChange={(e) => setCurrentStock(e.target.value)}
                required
            />

            <label htmlFor="dailyDemand">Expected Daily Demand:</label>
            <input
                type="number"
                id="dailyDemand"
                name="dailyDemand"
                value={dailyDemand}
                onChange={(e) => setDailyDemand(e.target.value)}
                required
            />

            <button type="submit">Submit</button>

            {/* Display selected options for demonstration */}
            {selectedOptions.medicineName && (
                <div>
                    <h3>Selected Options:</h3>
                    <p>Medicine Name: {selectedOptions.medicineName}</p>
                    <p>Current Stock: {selectedOptions.currentStock}</p>
                    <p>Expected Daily Demand: {selectedOptions.dailyDemand}</p>
                </div>
            )}
        </form>
    );
};

export default UserInputForm;
