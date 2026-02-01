import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const Charts = ({ data }) => {
    if (!data || !data.equipment_records || data.equipment_records.length === 0) {
        return (
            <div className="charts-container">
                <p className="no-data">No data available for charts</p>
            </div>
        );
    }

    const equipment = data.equipment_records;

    // Prepare data for Equipment Type Distribution (Pie Chart)
    const typeDistribution = {};
    equipment.forEach(item => {
        typeDistribution[item.equipment_type] = (typeDistribution[item.equipment_type] || 0) + 1;
    });

    const pieData = {
        labels: Object.keys(typeDistribution),
        datasets: [{
            label: 'Equipment Count',
            data: Object.values(typeDistribution),
            backgroundColor: [
                '#1e40af',
                '#0891b2',
                '#f59e0b',
                '#10b981',
                '#8b5cf6',
                '#ef4444',
                '#ec4899',
                '#06b6d4',
            ],
            borderWidth: 2,
            borderColor: '#ffffff',
        }]
    };

    // Prepare data for Average Parameters by Type (Bar Chart)
    const avgByType = {};
    equipment.forEach(item => {
        if (!avgByType[item.equipment_type]) {
            avgByType[item.equipment_type] = {
                flowrate: [],
                pressure: [],
                temperature: []
            };
        }
        avgByType[item.equipment_type].flowrate.push(item.flowrate);
        avgByType[item.equipment_type].pressure.push(item.pressure);
        avgByType[item.equipment_type].temperature.push(item.temperature);
    });

    const types = Object.keys(avgByType);
    const avgFlowrates = types.map(type => {
        const values = avgByType[type].flowrate;
        return values.reduce((a, b) => a + b, 0) / values.length;
    });
    const avgPressures = types.map(type => {
        const values = avgByType[type].pressure;
        return values.reduce((a, b) => a + b, 0) / values.length;
    });
    const avgTemperatures = types.map(type => {
        const values = avgByType[type].temperature;
        return values.reduce((a, b) => a + b, 0) / values.length;
    });

    const barData = {
        labels: types,
        datasets: [
            {
                label: 'Avg Flowrate (L/min)',
                data: avgFlowrates,
                backgroundColor: '#1e40af',
            },
            {
                label: 'Avg Pressure (bar)',
                data: avgPressures,
                backgroundColor: '#f59e0b',
            },
            {
                label: 'Avg Temperature (°C)',
                data: avgTemperatures,
                backgroundColor: '#ef4444',
            }
        ]
    };

    // Prepare data for Parameter Trends (Line Chart) - First 20 equipment
    const lineLabels = equipment.slice(0, 20).map(item => item.equipment_name);
    const lineFlowrates = equipment.slice(0, 20).map(item => item.flowrate);
    const linePressures = equipment.slice(0, 20).map(item => item.pressure);
    const lineTemperatures = equipment.slice(0, 20).map(item => item.temperature);

    const lineData = {
        labels: lineLabels,
        datasets: [
            {
                label: 'Flowrate',
                data: lineFlowrates,
                borderColor: '#1e40af',
                backgroundColor: 'rgba(30, 64, 175, 0.1)',
                tension: 0.4,
            },
            {
                label: 'Pressure',
                data: linePressures,
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                tension: 0.4,
            },
            {
                label: 'Temperature',
                data: lineTemperatures,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                tension: 0.4,
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
            }
        }
    };

    return (
        <div className="charts-container">
            <h2>Data Visualization</h2>
            
            <div className="charts-grid">
                {/* Pie Chart */}
                <div className="chart-card">
                    <h3>Equipment Type Distribution</h3>
                    <div className="chart-wrapper">
                        <Pie data={pieData} options={chartOptions} />
                    </div>
                </div>

                {/* Bar Chart */}
                <div className="chart-card">
                    <h3>Average Parameters by Type</h3>
                    <div className="chart-wrapper">
                        <Bar data={barData} options={chartOptions} />
                    </div>
                </div>

                {/* Line Chart */}
                <div className="chart-card full-width">
                    <h3>Parameter Trends (First 20 Equipment)</h3>
                    <div className="chart-wrapper">
                        <Line data={lineData} options={chartOptions} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Charts;