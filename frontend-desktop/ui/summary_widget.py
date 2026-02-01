from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class SummaryWidget(QWidget):
    """Widget for displaying summary statistics."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Summary Statistics")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Stats cards container
        self.stats_layout = QHBoxLayout()
        
        # Create stat cards
        self.total_card = self.create_stat_card("Total Equipment", "0", "#1e40af")
        self.flowrate_card = self.create_stat_card("Avg Flowrate", "0 L/min", "#0891b2")
        self.pressure_card = self.create_stat_card("Avg Pressure", "0 bar", "#f59e0b")
        self.temp_card = self.create_stat_card("Avg Temperature", "0 °C", "#ef4444")
        
        self.stats_layout.addWidget(self.total_card)
        self.stats_layout.addWidget(self.flowrate_card)
        self.stats_layout.addWidget(self.pressure_card)
        self.stats_layout.addWidget(self.temp_card)
        
        layout.addLayout(self.stats_layout)
        
        # Equipment type distribution
        self.type_label = QLabel("Equipment Type Distribution")
        type_font = QFont()
        type_font.setPointSize(12)
        type_font.setBold(True)
        self.type_label.setFont(type_font)
        layout.addWidget(self.type_label)
        
        self.type_list = QLabel("No data available")
        self.type_list.setWordWrap(True)
        self.type_list.setStyleSheet("""
            QLabel {
                padding: 15px;
                background: #f8fafc;
                border-radius: 5px;
                border: 1px solid #e2e8f0;
            }
        """)
        layout.addWidget(self.type_list)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_stat_card(self, label, value, color):
        """Create a stat card widget."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        card_layout = QVBoxLayout()
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: white; font-size: 12px;")
        card_layout.addWidget(label_widget)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        value_widget.setObjectName("value")
        card_layout.addWidget(value_widget)
        
        card.setLayout(card_layout)
        return card
    
    def update_summary(self, data):
        """Update summary statistics."""
        stats = data.get('summary_stats', {})
        
        self.update_card_value(self.total_card, str(stats.get('total_count', 0)))
        self.update_card_value(self.flowrate_card, f"{stats.get('avg_flowrate', 0):.2f} L/min")
        self.update_card_value(self.pressure_card, f"{stats.get('avg_pressure', 0):.2f} bar")
        self.update_card_value(self.temp_card, f"{stats.get('avg_temperature', 0):.2f} °C")
        
        equipment_types = stats.get('equipment_types', {})
        if equipment_types:
            type_text = "\n".join([f"{k}: {v}" for k, v in equipment_types.items()])
            self.type_list.setText(type_text)
        else:
            self.type_list.setText("No type distribution available")
    
    def update_card_value(self, card, value):
        """Update the value in a stat card."""
        value_label = card.findChild(QLabel, "value")
        if value_label:
            value_label.setText(value)
    
    def clear_summary(self):
        """Clear all summary data."""
        self.update_card_value(self.total_card, "0")
        self.update_card_value(self.flowrate_card, "0 L/min")
        self.update_card_value(self.pressure_card, "0 bar")
        self.update_card_value(self.temp_card, "0 °C")
        self.type_list.setText("No data available")