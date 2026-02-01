import React, { useState, useEffect } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import Summary from './components/Summary';
import Charts from './components/Charts';
import DataTable from './components/DataTable';
import History from './components/History';
import { uploadFile, getSummary, getDataset } from './services/api';
import { BarChart3 } from 'lucide-react';

function App() {
    const [currentData, setCurrentData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState('overview');

    // Load initial data
    useEffect(() => {
        loadLatestData();
    }, []);

    const loadLatestData = async () => {
        try {
            const data = await getSummary();
            setCurrentData(data);
        } catch (error) {
            console.error('Error loading data:', error);
        }
    };

    const handleUploadSuccess = async (file) => {
        setLoading(true);
        try {
            const result = await uploadFile(file);
            setCurrentData(result);
            setActiveTab('overview'); // Switch to overview after upload
            alert('File uploaded successfully!');
        } catch (error) {
            throw error; // Re-throw to be caught by FileUpload component
        } finally {
            setLoading(false);
        }
    };

    const handleSelectDataset = async (id) => {
        setLoading(true);
        try {
            const data = await getDataset(id);
            setCurrentData(data);
            setActiveTab('overview');
        } catch (error) {
            console.error('Error loading dataset:', error);
            alert('Failed to load dataset');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="app-header">
                <div className="header-content">
                    <div className="logo">
                        <BarChart3 size={32} />
                        <h1>Chemical Equipment Visualizer</h1>
                    </div>
                    <p className="tagline">Data-driven insights for chemical equipment management</p>
                </div>
            </header>

            {/* Navigation Tabs */}
            <nav className="nav-tabs">
                <button
                    className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
                    onClick={() => setActiveTab('overview')}
                >
                    Overview
                </button>
                <button
                    className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
                    onClick={() => setActiveTab('upload')}
                >
                    Upload
                </button>
                <button
                    className={`tab ${activeTab === 'history' ? 'active' : ''}`}
                    onClick={() => setActiveTab('history')}
                >
                    History
                </button>
            </nav>

            {/* Main Content */}
            <main className="main-content">
                {loading && (
                    <div className="loading-overlay">
                        <div className="spinner"></div>
                        <p>Processing data...</p>
                    </div>
                )}

                {activeTab === 'overview' && (
                    <div className="overview-tab">
                        <Summary data={currentData} />
                        <Charts data={currentData} />
                        <DataTable data={currentData} />
                    </div>
                )}

                {activeTab === 'upload' && (
                    <div className="upload-tab">
                        <FileUpload onUploadSuccess={handleUploadSuccess} />
                    </div>
                )}

                {activeTab === 'history' && (
                    <div className="history-tab">
                        <History onSelectDataset={handleSelectDataset} />
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="app-footer">
                <p>Chemical Equipment Parameter Visualizer © 2025</p>
            </footer>
        </div>
    );
}

export default App;