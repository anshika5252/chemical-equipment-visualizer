import React, { useState } from 'react';

const DataTable = ({ data }) => {
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    if (!data || !data.equipment_records || data.equipment_records.length === 0) {
        return (
            <div className="table-container">
                <p className="no-data">No equipment data available</p>
            </div>
        );
    }

    const equipment = data.equipment_records;
    
    // Pagination logic
    const totalPages = Math.ceil(equipment.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentEquipment = equipment.slice(startIndex, endIndex);

    const goToPage = (page) => {
        setCurrentPage(Math.max(1, Math.min(page, totalPages)));
    };

    return (
        <div className="table-container">
            <h2>Equipment Data</h2>
            
            <div className="table-info">
                <p>Showing {startIndex + 1}-{Math.min(endIndex, equipment.length)} of {equipment.length} items</p>
            </div>

            <div className="table-wrapper">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th>Equipment Name</th>
                            <th>Type</th>
                            <th>Flowrate (L/min)</th>
                            <th>Pressure (bar)</th>
                            <th>Temperature (°C)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {currentEquipment.map((item, index) => (
                            <tr key={item.id || index}>
                                <td className="equipment-name">{item.equipment_name}</td>
                                <td>
                                    <span className="type-badge">{item.equipment_type}</span>
                                </td>
                                <td>{item.flowrate.toFixed(1)}</td>
                                <td>{item.pressure.toFixed(1)}</td>
                                <td>{item.temperature.toFixed(1)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
                <div className="pagination">
                    <button
                        className="btn btn-small"
                        onClick={() => goToPage(currentPage - 1)}
                        disabled={currentPage === 1}
                    >
                        Previous
                    </button>
                    
                    <div className="page-numbers">
                        {[...Array(totalPages)].map((_, i) => (
                            <button
                                key={i}
                                className={`page-number ${currentPage === i + 1 ? 'active' : ''}`}
                                onClick={() => goToPage(i + 1)}
                            >
                                {i + 1}
                            </button>
                        ))}
                    </div>
                    
                    <button
                        className="btn btn-small"
                        onClick={() => goToPage(currentPage + 1)}
                        disabled={currentPage === totalPages}
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );
};

export default DataTable;