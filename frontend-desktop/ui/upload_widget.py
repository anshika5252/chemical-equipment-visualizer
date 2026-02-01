from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont

class UploadThread(QThread):
    """Background thread for file upload."""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        try:
            result = self.api_client.upload_file(self.file_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class UploadWidget(QWidget):
    """Widget for uploading CSV files."""
    
    upload_complete = pyqtSignal(dict)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.selected_file = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Upload Equipment Data")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel(
            "Select a CSV file with columns: Equipment Name, Type, "
            "Flowrate, Pressure, Temperature"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # File selection
        file_layout = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("padding: 10px; background: #f0f0f0; border-radius: 5px;")
        file_layout.addWidget(self.file_label)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e40af;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e3a8a;
            }
        """)
        file_layout.addWidget(browse_btn)
        
        layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = QPushButton("Upload")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                padding: 15px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #d1d5db;
            }
        """)
        layout.addWidget(self.upload_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def browse_file(self):
        """Open file dialog to select CSV."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path.split('/')[-1].split('\\')[-1])
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        """Upload selected file in background thread."""
        if not self.selected_file:
            return
        
        self.upload_btn.setEnabled(False)
        self.progress_bar.show()
        
        self.upload_thread = UploadThread(self.api_client, self.selected_file)
        self.upload_thread.finished.connect(self.on_upload_complete)
        self.upload_thread.error.connect(self.on_upload_error)
        self.upload_thread.start()
    
    def on_upload_complete(self, result):
        """Handle successful upload."""
        self.progress_bar.hide()
        self.upload_btn.setEnabled(True)
        
        QMessageBox.information(
            self,
            "Success",
            f"File uploaded successfully!\n{result.get('row_count', 0)} records processed."
        )
        
        self.selected_file = None
        self.file_label.setText("No file selected")
        self.upload_btn.setEnabled(False)
        
        self.upload_complete.emit(result)
    
    def on_upload_error(self, error_msg):
        """Handle upload error."""
        self.progress_bar.hide()
        self.upload_btn.setEnabled(True)
        
        QMessageBox.critical(
            self,
            "Upload Error",
            f"Failed to upload file:\n{error_msg}"
        )