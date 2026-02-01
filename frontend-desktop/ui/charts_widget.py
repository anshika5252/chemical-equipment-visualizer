from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ChartsWidget(QWidget):
    """Widget for displaying charts using Matplotlib."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Data Visualization")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Charts layout
        charts_layout = QHBoxLayout()
        
        # Create matplotlib figures
        self.fig1 = Figure(figsize=(5, 4), dpi=100)
        self.canvas1 = FigureCanvas(self.fig1)
        charts_layout.addWidget(self.canvas1)
        
        self.fig2 = Figure(figsize=(5, 4), dpi=100)
        self.canvas2 = FigureCanvas(self.fig2)
        charts_layout.addWidget(self.canvas2)
        
        layout.addLayout(charts_layout)
        
        # Bottom chart
        self.fig3 = Figure(figsize=(10, 4), dpi=100)
        self.canvas3 = FigureCanvas(self.fig3)
        layout.addWidget(self.canvas3)
        
        self.setLayout(layout)
    
    def update_charts(self, data):
        """Update all charts with new data."""
        equipment = data.get('equipment_records', [])
        
        if not equipment:
            return
        
        self.fig1.clear()
        self.fig2.clear()
        self.fig3.clear()
        
        self.create_pie_chart(equipment)
        self.create_bar_chart(equipment)
        self.create_line_chart(equipment)
        
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
    
    def create_pie_chart(self, equipment):
        """Create pie chart for equipment type distribution."""
        ax = self.fig1.add_subplot(111)
        
        type_counts = {}
        for item in equipment:
            eq_type = item['equipment_type']
            type_counts[eq_type] = type_counts.get(eq_type, 0) + 1
        
        ax.pie(
            type_counts.values(),
            labels=type_counts.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Set3.colors
        )
        ax.set_title('Equipment Type Distribution', fontweight='bold')
    
    def create_bar_chart(self, equipment):
        """Create bar chart for average parameters by type."""
        ax = self.fig2.add_subplot(111)
        
        type_data = {}
        for item in equipment:
            eq_type = item['equipment_type']
            if eq_type not in type_data:
                type_data[eq_type] = {'flowrate': [], 'pressure': [], 'temperature': []}
            
            type_data[eq_type]['flowrate'].append(item['flowrate'])
            type_data[eq_type]['pressure'].append(item['pressure'])
            type_data[eq_type]['temperature'].append(item['temperature'])
        
        types = list(type_data.keys())
        avg_flowrates = [sum(type_data[t]['flowrate']) / len(type_data[t]['flowrate']) for t in types]
        
        x = range(len(types))
        ax.bar(x, avg_flowrates, color='#1e40af')
        ax.set_xlabel('Equipment Type')
        ax.set_ylabel('Avg Flowrate (L/min)')
        ax.set_title('Average Flowrate by Type', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(types, rotation=45, ha='right')
        
        self.fig2.tight_layout()
    
    def create_line_chart(self, equipment):
        """Create line chart for parameter trends."""
        ax = self.fig3.add_subplot(111)
        
        sample = equipment[:20]
        names = [item['equipment_name'] for item in sample]
        flowrates = [item['flowrate'] for item in sample]
        pressures = [item['pressure'] for item in sample]
        temperatures = [item['temperature'] for item in sample]
        
        x = range(len(sample))
        
        ax.plot(x, flowrates, marker='o', label='Flowrate', color='#1e40af')
        ax.plot(x, pressures, marker='s', label='Pressure', color='#f59e0b')
        ax.plot(x, temperatures, marker='^', label='Temperature', color='#ef4444')
        
        ax.set_xlabel('Equipment')
        ax.set_ylabel('Value')
        ax.set_title('Parameter Trends (First 20 Equipment)', fontweight='bold')
        ax.set_xticks(x[::2])
        ax.set_xticklabels([names[i] for i in range(0, len(names), 2)], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        self.fig3.tight_layout()
    
    def clear_charts(self):
        """Clear all charts."""
        self.fig1.clear()
        self.fig2.clear()
        self.fig3.clear()
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()