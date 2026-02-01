from django.urls import path
from .views import (
    FileUploadView, 
    SummaryView, 
    HistoryView,
    DatasetDetailView,
    GenerateReportView
)

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('history/', HistoryView.as_view(), name='history'),
    path('dataset/<int:pk>/', DatasetDetailView.as_view(), name='dataset-detail'),
    path('report/<int:pk>/', GenerateReportView.as_view(), name='generate-report'),
]