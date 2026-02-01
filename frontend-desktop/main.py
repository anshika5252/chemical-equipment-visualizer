import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from services.api_client import APIClient

def main():
    """Entry point for the desktop application."""
    app = QApplication(sys.argv)
    
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("Your Organization")
    
    api_client = APIClient()
    
    window = MainWindow(api_client)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()