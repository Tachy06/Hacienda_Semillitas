from django.urls import path
from .views import *

urlpatterns = [
    path('adminPanel/', AdminCollegueView.as_view(), name='Admin'),
    path('viewProductsAdmin/', viewProductsAdmin.as_view(), name='ViewProductsAdmin'),
    path('deleteInvoice/<int:invoice_id>/', deleteAvoiceAdmin.as_view(), name='DeleteInvoice'),
    path('deleteProductsAdmin/<int:product_id>/', DeleteProductAdmin.as_view(), name='DeleteProductsAdmin'),
    path('view_all_companies/', viewAllCompaniesAdmin.as_view(), name='ViewAllCompanies'),
    path('createSuperAdmin/', CreateSuperAdmin.as_view(), name='CreateSuperAdmin'),

]