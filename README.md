# chemical-equipment-visualizer


A hybrid web and desktop application for analyzing and visualizing chemical equipment parameters.

##  Features

- CSV file upload and processing
- Real-time data visualization with interactive charts
- Summary statistics and analytics
- PDF report generation
- Web and desktop interfaces
- Upload history management (last 5 datasets)

##  Tech Stack

**Backend:**
- Django 4.2.7
- Django REST Framework
- Pandas
- ReportLab (PDF generation)

**Frontend (Web):**
- React 18
- Chart.js
- Axios
- Lucide React (icons)

**Frontend (Desktop):**
- PyQt5
- Matplotlib
- Requests

##  Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### React Frontend Setup
```bash
cd frontend-web
npm install
npm start
```

### Desktop App Setup
```bash
cd frontend-desktop
python -m venv venv
venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
python main.py
```

## Usage

1. Start Django backend 
2. Start React frontend 
3. run desktop app
4. Upload CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature
5. View data visualizations and statistics

## Sample Data

Use `sample_equipment_data.csv` for testing.

##  Demo

Google drive link: https://drive.google.com/file/d/1D9rbh7fKQ2eiuVPcyM_vAepnMiTBGIUi/view?usp=sharing

## Screenshots

Frontend-Web
File Upload :
<img width="1919" height="1043" alt="Screenshot 2026-02-01 180601" src="https://github.com/user-attachments/assets/847c8b6e-2595-4080-886b-e7a3902ca75c" />

The Webpage:
<img width="1909" height="1010" alt="Screenshot 2026-02-01 180625" src="https://github.com/user-attachments/assets/ba103d34-e81d-45b1-a064-5ba3384ffd6b" />
<img width="1917" height="1004" alt="Screenshot 2026-02-01 180722" src="https://github.com/user-attachments/assets/34c23120-a161-44ff-acb5-da15b5e1d3e4" />
<img width="1876" height="1010" alt="Screenshot 2026-02-01 180736" src="https://github.com/user-attachments/assets/068ca2e2-68f3-45ac-b567-33b9a0774ec9" />
<img width="1893" height="986" alt="Screenshot 2026-02-01 180751" src="https://github.com/user-attachments/assets/c8dd032a-f84e-4a54-9e0a-08f1b5b727b2" />

Pdf report:
<img width="768" height="855" alt="image" src="https://github.com/user-attachments/assets/cd12ce53-fa1b-4b67-847c-ba059418b05f" />

Frontend-Desktop
File Upload:
<img width="1916" height="1005" alt="Screenshot 2026-02-01 190904" src="https://github.com/user-attachments/assets/12dcee52-cc2b-40bf-aeb1-13794973adaa" />

The Desktop Main Page:
<img width="1909" height="994" alt="Screenshot 2026-02-01 190828" src="https://github.com/user-attachments/assets/e137f41c-919a-4dd3-8708-89a01557cfc2" />


##  Author

Anshika Jain - https://github.com/anshika5252

##  License

This project was created for educational purposes.
