from django.urls import path
from .views import *

urlpatterns = [
    path('adminPanel/', AdminCollegueView.as_view(), name='Admin'),
    path('viewProductsAdmin/', viewProductsAdmin.as_view(), name='ViewProductsAdmin'),
    path('deleteInvoice/<int:invoice_id>/', deleteAvoiceAdmin.as_view(), name='DeleteInvoice'),

]