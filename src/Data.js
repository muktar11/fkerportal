// salesData.js

let UserData = [];

export const fetchSalesData = async () => {
  try {
    const response = await fetch("http://192.168.100.16:8000/commerce/sales-order-monthly-sales-target");
    const salesData = await response.json();

    UserData = [
      {
        id: 1,
        Area: 'Area1',
        userGain: salesData.aggregated_data_by_route.Area1.WebCustomer.sales_target,
        userLost: salesData.aggregated_data_by_route.Area1.WebCustomer.total_sales,
      },
      {
        id: 2,
        Area: 'Area2',
        userGain: salesData.aggregated_data_by_route.Area2.WebCustomer.sales_target,
        userLost: salesData.aggregated_data_by_route.Area2.WebCustomer.total_sales,
      },
      {
        id: 3,
        Area: 'Area3',
        userGain: salesData.aggregated_data_by_route.Area3.WebCustomer.sales_target,
        userLost: salesData.aggregated_data_by_route.Area3.WebCustomer.total_sales,
      },
      {
        id: 4,
        Area: 'EastMarket',
        userGain: salesData.aggregated_data_by_route.EastMarket.WebCustomer.sales_target,
        userLost: salesData.aggregated_data_by_route.EastMarket.WebCustomer.total_sales,
      },
      {
        id: 5,
        Area: 'AdissAbabaMarket',
        userGain: salesData.aggregated_data_by_route.AdissAbabaMarket.WebCustomer.sales_target,
        userLost: salesData.aggregated_data_by_route.AdissAbabaMarket.WebCustomer.total_sales,
      },
      {
        id: 6,
        Area: 'AdissAbabaMarket2',
        userGain: salesData.aggregated_data_by_route.AdissAbabaMarket2.WebCustomer.sales_target,
        userLost: salesData.aggregated_data_by_route.AdissAbabaMarket2.WebCustomer.total_sales,
      },
      {
        id: 7,
        Area: 'Area8',
        userGain: salesData.aggregated_data_by_route.Area8.WebCustomer.sales_target,
        userLost: salesData.aggregated_data_by_route.Area8.WebCustomer.total_sales,
      },

      // ... (other user data objects)
    ];

    console.log("Updated UserData:", UserData);
    
    return UserData; // Return updated UserData

  } catch (error) {
    console.error("Error fetching sales data:", error);
    return []; // Return an empty array in case of an error
  }
};

// Call the fetchSalesData function to get and update the data
export default UserData;
