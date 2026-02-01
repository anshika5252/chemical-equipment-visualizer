from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Dataset, EquipmentData
from .serializers import DatasetSerializer, DatasetListSerializer
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd
import io

@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        print("=" * 60)
        print("UPLOAD REQUEST RECEIVED")
        print("FILES:", request.FILES)
        print("=" * 60)
        
        file = request.FILES.get('file')
        
        if not file:
            print("ERROR: No file in request")
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"File received: {file.name}, size: {file.size}")
        
        if not file.name.endswith('.csv'):
            return Response({'error': 'Only CSV files allowed'}, status=status.HTTP_400_BAD_REQUEST)
        
        dataset = None
        try:
            # Create dataset
            dataset = Dataset.objects.create(
                filename=file.name,
                row_count=0,
                summary_stats={},
                file=file
            )
            print(f"Dataset created with ID: {dataset.id}")
            
            # Read CSV
            file_content = file.read()
            try:
                csv_string = file_content.decode('utf-8')
            except:
                csv_string = file_content.decode('latin-1')
            
            # Instead of reading a raw string, use the uploaded file object directly
            csv_file = request.FILES['file']
# Ensure we start reading from the very first character
            csv_file.seek(0) 
            df = pd.read_csv(csv_file)
            
            print("CSV Columns:", list(df.columns))
            print("CSV Shape:", df.shape)
            
            # Check required columns
            required = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing = [col for col in required if col not in df.columns]
            if missing:
                raise ValueError(f"Missing columns: {missing}")
            
            # Calculate summary
            summary = {
                'total_count': int(len(df)),
                'avg_flowrate': float(df['Flowrate'].mean()),
                'avg_pressure': float(df['Pressure'].mean()),
                'avg_temperature': float(df['Temperature'].mean()),
                'equipment_types': {str(k): int(v) for k, v in df['Type'].value_counts().to_dict().items()},
            }
            
            print(f"Processing {len(df)} rows...")
            
            # Create equipment records
            for idx, row in df.iterrows():
                EquipmentData.objects.create(
                    dataset=dataset,
                    equipment_name=str(row['Equipment Name']).strip(),
                    equipment_type=str(row['Type']).strip(),
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                )
            
            # Update dataset
            dataset.row_count = summary['total_count']
            dataset.summary_stats = summary
            dataset.save()
            
            print(f"✅ Upload successful! {summary['total_count']} records saved")
            print("=" * 60)
            
            # Keep only last 5
            old_datasets = Dataset.objects.all().order_by('-upload_date')[5:]
            for old in old_datasets:
                try:
                    old.file.delete()
                except:
                    pass
                old.delete()
            
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print("❌ ERROR:", str(e))
            import traceback
            traceback.print_exc()
            
            if dataset:
                try:
                    dataset.delete()
                except:
                    pass
            
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SummaryView(APIView):
    def get(self, request):
        dataset = Dataset.objects.first()
        if not dataset:
            return Response({'message': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)

class HistoryView(APIView):
    def get(self, request):
        datasets = Dataset.objects.all()[:5]
        serializer = DatasetListSerializer(datasets, many=True)
        return Response(serializer.data)

class DatasetDetailView(APIView):
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

class GenerateReportView(APIView):
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            title = Paragraph(f"Equipment Report: {dataset.filename}", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))
            
            summary_text = f"""
            <b>Upload Date:</b> {dataset.upload_date.strftime('%Y-%m-%d %H:%M')}<br/>
            <b>Total Records:</b> {dataset.row_count}<br/>
            <b>Average Flowrate:</b> {dataset.summary_stats.get('avg_flowrate', 'N/A'):.2f}<br/>
            <b>Average Pressure:</b> {dataset.summary_stats.get('avg_pressure', 'N/A'):.2f}<br/>
            <b>Average Temperature:</b> {dataset.summary_stats.get('avg_temperature', 'N/A'):.2f}<br/>
            """
            summary = Paragraph(summary_text, styles['Normal'])
            elements.append(summary)
            elements.append(Spacer(1, 12))
            
            equipment_data = EquipmentData.objects.filter(dataset=dataset)[:20]
            table_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
            for eq in equipment_data:
                table_data.append([
                    eq.equipment_name,
                    eq.equipment_type,
                    f"{eq.flowrate:.2f}",
                    f"{eq.pressure:.2f}",
                    f"{eq.temperature:.2f}"
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
            
            doc.build(elements)
            buffer.seek(0)
            
            return FileResponse(buffer, as_attachment=True, filename=f'report_{dataset.id}.pdf')
            
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)