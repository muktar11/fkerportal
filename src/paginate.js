import axios from 'axios';
import React, { useState, useEffect } from 'react';
import ReactTable from 'react-table-6';
import 'react-table-6/react-table.css';
import ReactPaginate from 'react-paginate';
import { CSVLink } from 'react-csv';

const PaginatedTable = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const fetchData = async (page = 0) => {
    try {
      const response = await axios.get(`http://192.168.100.205:8000/commerce/finance-inventory-lists?page=${page}`);
      setData(response.data); // Set the fetched data directly
      setTotalPages(Math.ceil(response.data.length / 10)); // Assuming 10 items per page
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlePageClick = (selectedPage) => {
    setCurrentPage(selectedPage.selected);
    fetchData(selectedPage.selected);
  };

  const downloadAllData = async () => {
    try {
      // Use the fetched data directly for CSV generation
      const csvData = data.map(item => ({
        // Map your fields here
        field1: item.customers_name,
        field2: item.customers_id,
        field2: item.sales_Route,
        // Add other fields accordingly
      }));

      // Trigger download
      const csvContent = CSVLink(csvData, { headers: [ /* Headers here */ ] }); // Adjust headers if needed
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'data.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Error downloading data: ', error);
    }
  };

  const columns = [
    {
      Header: 'Customer Name',
      accessor: 'customers_name', // Key in the data object
    },
    {
      Header: 'Customer ID',
      accessor: 'customers_id',
    },
    {
      Header: 'Sales Route',
      accessor: 'sales_Route',
    },
    {
      Header: 'Ledger Balance',
      accessor: 'LedgerBalance',
    },

    

    
    // Add more columns as needed following the same structure
  ];

  return (
    <div>
      <ReactTable
        data={data}
        columns={columns}
        defaultPageSize={10}
        className="-striped -highlight"
      />
      <ReactPaginate
        pageCount={totalPages}
        pageRangeDisplayed={5}
        marginPagesDisplayed={2}
        onPageChange={handlePageClick}
        containerClassName={'pagination'}
        activeClassName={'active'}
      />
      <button onClick={downloadAllData}>Download All Data</button>
    </div>
  );
};

export default PaginatedTable;
