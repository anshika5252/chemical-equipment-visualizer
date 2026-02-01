import React from 'react';
import { Activity, Thermometer, Gauge, Droplets } from 'lucide-react';

const Summary = ({ data }) => {
    if (!data || !data.summary_stats) {
        return (
            <div className="summary-container">
                <p className="no-data">No data available. Upload a CSV file to see statistics.</p>
            </div>
        );
    }

    const stats = data.summary_stats;

    const statCards = [
        {
            icon: Activity,
            label: 'Total Equipment',
            value: stats.total_count,
            unit: 'items',
            color: '#1e40af'
        },
        {
            icon: Droplets,
            label: 'Avg Flowrate',
            value: stats.avg_flowrate?.toFixed(2) || 'N/A',
            unit: 'L/min',
            color: '#0891b2'
        },
        {
            icon: Gauge,
            label: 'Avg Pressure',
            value: stats.avg_pressure?.toFixed(2) || 'N/A',
            unit: 'bar',
            color: '#f59e0b'
        },
        {
            icon: Thermometer,
            label: 'Avg Temperature',
            value: stats.avg_temperature?.toFixed(2) || 'N/A',
            unit: '°C',
            color: '#ef4444'
        }
    ];

    return (
        <div className="summary-container">
            <h2>Summary Statistics</h2>
            <div className="stat-grid">
                {statCards.map((stat, index) => {
                    const Icon = stat.icon;
                    return (
                        <div
                            key={index}
                            className="stat-card"
                            style={{ '--card-color': stat.color }}
                        >
                            <div className="stat-icon">
                                <Icon size={32} />
                            </div>
                            <div className="stat-content">
                                <p className="stat-label">{stat.label}</p>
                                <p className="stat-value">
                                    {stat.value} <span className="stat-unit">{stat.unit}</span>
                                </p>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Equipment Type Distribution */}
            {stats.equipment_types && (
                <div className="type-distribution">
                    <h3>Equipment Type Distribution</h3>
                    <div className="type-list">
                        {Object.entries(stats.equipment_types).map(([type, count]) => (
                            <div key={type} className="type-item">
                                <span className="type-name">{type}</span>
                                <span className="type-count">{count}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default Summary;