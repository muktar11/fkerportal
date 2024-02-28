import React, { useEffect, useState } from "react";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { Box, FormControl, InputLabel, MenuItem, Select, Typography } from "@mui/material";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";
import { useParams } from "react-router-dom";

const PriceHistoryWareHouse = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [customerData, setCustomerData] = useState([]);
  const [page, setPage] = useState(1);
  const [selectedSalesRoute, setSelectedSalesRoute] = useState(''); // State for selected sales route
  const [selectedWarehouse, setSelectedWarehouse] = useState(''); // State for selected warehouse
 
  useEffect(() => {
    const fetchData = async () => {
      try {
        let apiUrl = process.env.REACT_APP_API_URL + '/commerce/get-latest-price/';
        
        if (selectedSalesRoute && selectedWarehouse) {
          apiUrl += `${selectedSalesRoute}/${selectedWarehouse}/`;
        } else if (selectedSalesRoute) {
          apiUrl += `${selectedSalesRoute}/`;
        } else if (selectedWarehouse) {
          apiUrl += `/${selectedWarehouse}/`;
        }
  
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
  
        const data = await response.json();
        console.log('Fetched data:', data); // Log fetched data
        setCustomerData(data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, [page, selectedSalesRoute, selectedWarehouse]);


  const columns = [
    { field: "_id", headerName: "ID", flex: 0.5 },
    { field: "sales_Route", headerName: "Sales Route", flex: 1 },
    { field: "Q", headerName: "0.35ml", flex: 1, cellClassName: "name-column--cell" },
    { field: "H", headerName: "0.6ml", flex: 1, cellClassName: "name-column--cell" },
    { field: "ONE", headerName: "1L", flex: 1, cellClassName: "name-column--cell" },
    { field: "TWO", headerName: "2L", flex: 1, cellClassName: "name-column--cell" },
    { field: "TransportationFee", headerName: "TransportationFee/Km", flex: 1 },
    { field: "created_at", headerName: "Created At", flex: 1 },  
  ];

  
    // ... other columns
  const getRowId = (row) => row._id;

  return (
    <Box m="20px">
      <Header
        title="Access WareHouse Price History and Market"
        subtitle="List of prices per warehouse "
      />
      <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
        <InputLabel id="area-label">Select Area</InputLabel>
        <Select
          labelId="area-label"
          id="area-select"
          label="Select Area"
          value={selectedSalesRoute}
          onChange={(e) => setSelectedSalesRoute(e.target.value)}
        >
          <MenuItem value=""><em>All</em></MenuItem>
      <MenuItem value="Area1">Area1</MenuItem>
      <MenuItem value="Area1B">Area1B</MenuItem>
      <MenuItem value="Area2">Area2</MenuItem>
      <MenuItem value="Area3">Area3</MenuItem>
      <MenuItem value="EastMarket">EastMarket</MenuItem>
      <MenuItem value="AdissAbabaMarket">AdissAbabaMarket</MenuItem>
      <MenuItem value="AdissAbabaMarket2">AdissAbabaMarket2</MenuItem>
      <MenuItem value="Area8">Area8</MenuItem>
      
        </Select>
      </FormControl>

      <FormControl sx={{ m: 1, minWidth: 220 }} size="small">
        <InputLabel id="warehouse-label">Select WareHouse</InputLabel>
        <Select
          labelId="warehouse-label"
          id="warehouse-select"
          label="Select Warehouse"
          value={selectedWarehouse}
          onChange={(e) => setSelectedWarehouse(e.target.value)}
        >
          <MenuItem value=""><em>All</em></MenuItem>
          <MenuItem value="AdissAbaba">Adiss Ababa</MenuItem>
        <MenuItem value="Agena">Agena</MenuItem>
        <MenuItem value="Wolketie">Wolketie</MenuItem>

        </Select>
      </FormControl>

      <Box
        m=" 0 0 0"
        height="100vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
            height: "10vh", // Set the desired height for the customer_name field
        
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
            height: "10vh", // Set the desired height for the customer_name field
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
          "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
            color: `${colors.grey[100]} !important`,
          },
        }}
      >
         <DataGrid
        rows={customerData}
        columns={columns}
        components={{ Toolbar: GridToolbar }}
        getRowId={getRowId}
        pagination
        pageSize={10}
        onPageChange={(newPage) => setPage(newPage + 1)}
        />
      </Box>
    </Box>
  );
};

export default PriceHistoryWareHouse;
