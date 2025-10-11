from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from bills import helper

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    # add accouts app urls
    path('accounts/', include('accounts.urls')),  
    # You can add more apps later:
    path('items/', include('items.urls')),
    # add bills app urls
    path('bills/', include('bills.urls')),

    # Admin side 
    # path('admin/create/', helper.create_bill, name='admin_create_bill'),
    path('admino/all-bills/', helper.total_bills, name='admin_all_bills'),   
    path('admino/add-employee/', helper.add_employee, name='add_employee'),
    path('admino/employees/', helper.all_employees, name='all_employees'),
    path('admino/add-item/', helper.add_item, name='add_item'),
    path('admino/all-items/', helper.all_items, name='all_items'),
    path('admino/edit-employee/<int:user_id>/', helper.edit_employee, name='edit_employee'),
    path('admino/view-employee/<int:user_id>/', helper.view_employee, name='view_employee'),
    path('admino/delete-employee/<int:user_id>/', helper.delete_employee, name='delete_employee'),
    path('admino/edit-item/<int:item_id>/', helper.edit_item, name='edit_item'),
    path('admino/delete-item/<int:item_id>/', helper.delete_item, name='delete_item'),
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
