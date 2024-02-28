// ChartJSS.js

import { useState, useEffect } from "react";
import BarChart from "./BarChart";
import { fetchSalesData } from "./Data";

function ChartJSS() {
  const [userData, setUserData] = useState({
    labels: [],
    datasets: [
      {
        label: "Sales Completed",
        data: [],
        backgroundColor: ["rgba(75,192,192,1)"],
        borderColor: "black",
        borderWidth: 2,
      },
    ],
  });

  useEffect(() => {
    // Fetch sales data and update the chart data
    const fetchData = async () => {
      const updatedUserData = await fetchSalesData();
      setUserData({
        labels: updatedUserData.map((data) => data.Area),
        datasets: [
          {
            label: "Sales Completed",
            data: updatedUserData.map((data) => data.userGain),
            backgroundColor: ["rgba(75,192,192,1)"],
            borderColor: "black",
            borderWidth: 2,
          },
        ],
      });
    };

    fetchData();
  }, []); // Run once when the component mounts

  return (
    <div className="App">
      <div style={{ width: 700 }}>
        <BarChart chartData={userData} />
      </div>
    </div>
  );
}

export default ChartJSS;
