import React, { useState } from 'react';
import { Upload, FileCheck, AlertCircle } from 'lucide-react';

const FileUpload = ({ onUploadSuccess }) => {
    const [file, setFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);

    // Handle file selection
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        validateAndSetFile(selectedFile);
    };

    // Validate file
    const validateAndSetFile = (selectedFile) => {
        if (!selectedFile) return;
        
        if (!selectedFile.name.endsWith('.csv')) {
            setError('Please upload a CSV file');
            return;
        }
        
        if (selectedFile.size > 5 * 1024 * 1024) { // 5MB limit
            setError('File size must be less than 5MB');
            return;
        }
        
        setFile(selectedFile);
        setError(null);
    };

    // Drag and drop handlers
    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        
        const droppedFile = e.dataTransfer.files[0];
        validateAndSetFile(droppedFile);
    };

    // Upload file
    const handleUpload = async () => {
        if (!file) return;
        
        setUploading(true);
        setError(null);
        
        try {
            await onUploadSuccess(file);
            setFile(null); // Reset after success
        } catch (err) {
            setError(err.response?.data?.error || 'Upload failed. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="upload-container">
            <h2>Upload Equipment Data</h2>
            
            {/* Drag & Drop Zone */}
            <div
                className={`upload-zone ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                {!file ? (
                    <>
                        <Upload size={48} className="upload-icon" />
                        <p className="upload-text">
                            Drag & drop your CSV file here
                        </p>
                        <p className="upload-subtext">or</p>
                        <label className="file-label">
                            <input
                                type="file"
                                accept=".csv"
                                onChange={handleFileChange}
                                style={{ display: 'none' }}
                            />
                            <span className="btn btn-secondary">Browse Files</span>
                        </label>
                    </>
                ) : (
                    <>
                        <FileCheck size={48} className="upload-icon success" />
                        <p className="upload-text">{file.name}</p>
                        <p className="upload-subtext">
                            {(file.size / 1024).toFixed(2)} KB
                        </p>
                        <div className="upload-actions">
                            <button
                                className="btn btn-primary"
                                onClick={handleUpload}
                                disabled={uploading}
                            >
                                {uploading ? 'Uploading...' : 'Upload'}
                            </button>
                            <button
                                className="btn btn-secondary"
                                onClick={() => setFile(null)}
                                disabled={uploading}
                            >
                                Clear
                            </button>
                        </div>
                    </>
                )}
            </div>

            {/* Error Message */}
            {error && (
                <div className="error-message">
                    <AlertCircle size={20} />
                    <span>{error}</span>
                </div>
            )}

            {/* Instructions */}
            <div className="upload-info">
                <h4>CSV Format Requirements:</h4>
                <ul>
                    <li>Columns: Equipment Name, Type, Flowrate, Pressure, Temperature</li>
                    <li>File size: Maximum 5MB</li>
                    <li>Format: .csv only</li>
                </ul>
            </div>
        </div>
    );
};

export default FileUpload;