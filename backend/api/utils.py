import pandas as pd
import io
from .models import Dataset, EquipmentData

def process_csv_file(csv_file, dataset_instance):
    """Process uploaded CSV and extract statistics."""
    
    # Read the file content
    file_content = csv_file.read()
    
    # Decode to string
    try:
        csv_string = file_content.decode('utf-8')
    except:
        csv_string = file_content.decode('latin-1')
    
    # Read into DataFrame
    df = pd.read_csv(io.StringIO(csv_string))
    
    # Print for debugging
    print("Columns found:", df.columns.tolist())
    print("First row:", df.head(1).to_dict())
    
    # Calculate summary statistics
    summary = {
        'total_count': int(len(df)),
        'avg_flowrate': float(df['Flowrate'].mean()),
        'avg_pressure': float(df['Pressure'].mean()),
        'avg_temperature': float(df['Temperature'].mean()),
        'equipment_types': {str(k): int(v) for k, v in df['Type'].value_counts().to_dict().items()},
    }
    
    # Create equipment records
    equipment_records = []
    for idx, row in df.iterrows():
        equipment_records.append(
            EquipmentData(
                dataset=dataset_instance,
                equipment_name=str(row['Equipment Name']).strip(),
                equipment_type=str(row['Type']).strip(),
                flowrate=float(row['Flowrate']),
                pressure=float(row['Pressure']),
                temperature=float(row['Temperature'])
            )
        )
    
    # Bulk create all records
    EquipmentData.objects.bulk_create(equipment_records)
    
    return summary

def maintain_dataset_limit():
    """Keep only the last 5 datasets."""
    datasets = Dataset.objects.all().order_by('-upload_date')
    if datasets.count() > 5:
        old_datasets = datasets[5:]
        for dataset in old_datasets:
            try:
                dataset.file.delete()
            except:
                pass
            dataset.delete()