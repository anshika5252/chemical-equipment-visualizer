from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TableWidget(QWidget):
    """Widget for displaying equipment data in a table."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Equipment Data")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate (L/min)", 
            "Pressure (bar)", "Temperature (°C)"
        ])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 5px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #1e40af;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def update_data(self, data):
        """Update table with new data."""
        equipment = data.get('equipment_records', [])
        
        self.table.setRowCount(len(equipment))
        
        for row, item in enumerate(equipment):
            self.table.setItem(row, 0, QTableWidgetItem(item['equipment_name']))
            self.table.setItem(row, 1, QTableWidgetItem(item['equipment_type']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item['flowrate']:.1f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['pressure']:.1f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{item['temperature']:.1f}"))
    
    def clear_data(self):
        """Clear all table data."""
        self.table.setRowCount(0)