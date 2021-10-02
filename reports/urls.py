from django.urls import path
from .views import(
    UploadTemplateview,
    create_report_view,
    ReportListView,
    ReportDetailtView,
    render_pdf_view ,
    UploadTemplateview , 
    csv_upload_view,        
)   

app_name = 'reports'

urlpatterns = [
    path('',ReportListView.as_view(),name='main'),
    path('save/',create_report_view,name='create-report'),
    path('upload/',csv_upload_view, name='upload'),#for csv
    path('from_file/',UploadTemplateview.as_view(),name='from-file'),#for csv
    path('<pk>/',ReportDetailtView.as_view(),name='detail'),
    path('<pk>/pdf/',render_pdf_view,name='pdf'),
]
