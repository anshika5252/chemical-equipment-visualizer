import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
import requests

class SimpleDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer - Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Title
        title = QLabel("Chemical Equipment Visualizer - Desktop Test")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px;")
        layout.addWidget(title)
        
        # Status label
        self.status_label = QLabel("Click button to test backend connection")
        self.status_label.setStyleSheet("padding: 20px;")
        layout.addWidget(self.status_label)
        
        # Test button
        test_btn = QPushButton("Test Backend Connection")
        test_btn.clicked.connect(self.test_backend)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e40af;
                color: white;
                padding: 15px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1e3a8a;
            }
        """)
        layout.addWidget(test_btn)
        
        layout.addStretch()
    
    def test_backend(self):
        try:
            response = requests.get('http://127.0.0.1:8000/api/summary/')
            if response.status_code == 200 or response.status_code == 404:
                self.status_label.setText("✅ Backend is running! Connection successful.")
                self.status_label.setStyleSheet("padding: 20px; color: green; font-size: 16px;")
            else:
                self.status_label.setText(f"⚠️ Backend responded with status: {response.status_code}")
                self.status_label.setStyleSheet("padding: 20px; color: orange; font-size: 16px;")
        except Exception as e:
            self.status_label.setText(f"❌ Cannot connect to backend: {str(e)}")
            self.status_label.setStyleSheet("padding: 20px; color: red; font-size: 16px;")

def main():
    app = QApplication(sys.argv)
    window = SimpleDesktopApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
