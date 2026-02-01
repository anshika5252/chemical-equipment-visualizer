import requests
from typing import Dict, List, Optional

class APIClient:
    """
    Client for communicating with Django backend.
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        
    def upload_file(self, file_path: str) -> Dict:
        """Upload CSV file to backend."""
        url = f"{self.base_url}/upload/"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            
        response.raise_for_status()
        return response.json()
    
    def get_summary(self) -> Dict:
        """Get summary of most recent dataset."""
        url = f"{self.base_url}/summary/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_history(self) -> List[Dict]:
        """Get list of all datasets (last 5)."""
        url = f"{self.base_url}/history/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_dataset(self, dataset_id: int) -> Dict:
        """Get specific dataset details."""
        url = f"{self.base_url}/dataset/{dataset_id}/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def download_report(self, dataset_id: int, save_path: str):
        """Download PDF report."""
        url = f"{self.base_url}/report/{dataset_id}/"
        response = requests.get(url)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)