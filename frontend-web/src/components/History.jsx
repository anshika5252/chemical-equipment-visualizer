import React, { useState, useEffect } from 'react';
import { Clock, Download, Eye } from 'lucide-react';
import { getHistory, downloadReport } from '../services/api';

const History = ({ onSelectDataset }) => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const data = await getHistory();
            setHistory(data);
        } catch (error) {
            console.error('Error fetching history:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = async (id) => {
        try {
            await downloadReport(id);
        } catch (error) {
            console.error('Error downloading report:', error);
            alert('Failed to download report');
        }
    };

    if (loading) {
        return (
            <div className="history-container">
                <p>Loading history...</p>
            </div>
        );
    }

    if (history.length === 0) {
        return (
            <div className="history-container">
                <p className="no-data">No upload history available</p>
            </div>
        );
    }

    return (
        <div className="history-container">
            <h2>Upload History</h2>
            <p className="history-subtitle">Last 5 uploaded datasets</p>

            <div className="history-list">
                {history.map((dataset) => (
                    <div key={dataset.id} className="history-item">
                        <div className="history-info">
                            <h4 className="history-filename">{dataset.filename}</h4>
                            <div className="history-meta">
                                <span className="history-date">
                                    <Clock size={14} />
                                    {new Date(dataset.upload_date).toLocaleString()}
                                </span>
                                <span className="history-count">
                                    {dataset.row_count} records
                                </span>
                            </div>
                        </div>
                        
                        <div className="history-actions">
                            <button
                                className="btn btn-icon"
                                onClick={() => onSelectDataset(dataset.id)}
                                title="View dataset"
                            >
                                <Eye size={18} />
                            </button>
                            <button
                                className="btn btn-icon"
                                onClick={() => handleDownload(dataset.id)}
                                title="Download PDF report"
                            >
                                <Download size={18} />
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default History;