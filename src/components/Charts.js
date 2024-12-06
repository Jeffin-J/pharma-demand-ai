import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

const Charts = () => {
  const [chartData, setChartData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch processed data from the Flask backend
    const fetchChartData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/get-processed-data");
        if (!response.ok) throw new Error("Failed to fetch data.");
        const data = await response.json();

        // Prepare data for chart
        const labels = data.map((item) => item["Sale Date"]); // Replace with correct date key
        const stockLevels = data.map((item) => item["Units Sold"]); // Replace with correct stock key

        setChartData({
          labels,
          datasets: [
            {
              label: "Stock Levels Over Time",
              data: stockLevels,
              fill: false,
              borderColor: "#4caf50",
              tension: 0.1,
            },
          ],
        });

        setLoading(false);
      } catch (error) {
        console.error("Error fetching chart data:", error);
        setLoading(false);
      }
    };

    fetchChartData();
  }, []);

  if (loading) return <p>Loading chart data...</p>;

  return (
    <div style={{ margin: "20px" }}>
      <h2>Stock Forecast Chart</h2>
      <Line
        data={chartData}
        options={{
          responsive: true,
          plugins: {
            legend: {
              display: true,
              position: "top",
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Sale Date",
              },
            },
            y: {
              title: {
                display: true,
                text: "Units Sold",
              },
            },
          },
        }}
      />
    </div>
  );
};

export default Charts;
