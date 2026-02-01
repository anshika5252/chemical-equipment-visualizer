from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QStatusBar, QMenuBar, QAction, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from .upload_widget import UploadWidget
from .summary_widget import SummaryWidget
from .table_widget import TableWidget
from .charts_widget import ChartsWidget

class LoadDataThread(QThread):
    """Background thread for loading data."""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
    
    def run(self):
        try:
            result = self.api_client.get_summary()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.current_data = None
        self.init_ui()
        self.load_initial_data()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        self.create_menu_bar()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.tabs = QTabWidget()
        
        # Overview tab
        overview_widget = QWidget()
        overview_layout = QVBoxLayout()
        
        self.summary_widget = SummaryWidget()
        self.charts_widget = ChartsWidget()
        self.table_widget = TableWidget()
        
        overview_layout.addWidget(self.summary_widget)
        overview_layout.addWidget(self.charts_widget)
        overview_layout.addWidget(self.table_widget)
        overview_widget.setLayout(overview_layout)
        
        # Upload tab
        self.upload_widget = UploadWidget(self.api_client)
        self.upload_widget.upload_complete.connect(self.on_data_updated)
        
        self.tabs.addTab(overview_widget, "Overview")
        self.tabs.addTab(self.upload_widget, "Upload")
        
        layout.addWidget(self.tabs)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #f1f5f9;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #1e40af;
                color: white;
            }
        """)
    
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        refresh_action = QAction("Refresh Data", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_data)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def load_initial_data(self):
        """Load initial data when app starts."""
        self.status_bar.showMessage("Loading data...")
        
        self.load_thread = LoadDataThread(self.api_client)
        self.load_thread.finished.connect(self.on_data_loaded)
        self.load_thread.error.connect(self.on_load_error)
        self.load_thread.start()
    
    def on_data_loaded(self, data):
        """Handle successful data load."""
        self.current_data = data
        self.update_all_widgets(data)
        self.status_bar.showMessage("Data loaded successfully", 3000)
    
    def on_load_error(self, error_msg):
        """Handle data load error."""
        self.status_bar.showMessage("No data available", 3000)
    
    def on_data_updated(self, data):
        """Handle new data from upload."""
        self.current_data = data
        self.update_all_widgets(data)
        self.tabs.setCurrentIndex(0)
    
    def update_all_widgets(self, data):
        """Update all widgets with new data."""
        self.summary_widget.update_summary(data)
        self.charts_widget.update_charts(data)
        self.table_widget.update_data(data)
    
    def refresh_data(self):
        """Refresh data from backend."""
        self.load_initial_data()
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About",
            "Chemical Equipment Visualizer\n\n"
            "A hybrid web and desktop application for visualizing "
            "chemical equipment parameters.\n\n"
            "Built with PyQt5 and Django REST Framework"
        )