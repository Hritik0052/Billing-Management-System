from django.urls import path
from . import views
from . import utils

urlpatterns = [
    # Employee side 
    path('create/', views.create_bill, name='create_bill'),
    path('view/<int:bill_no>/', views.view_bill, name='view_bill'),
    path('all-bills/', views.bill_list, name='all_bills'),
    path('bill-reports/', views.bill_reports, name='bill_reports'),
    path('bills/download-report/', utils.download_bills_report, name='download_bills_report'),

]