from django.urls import path
from .views import *

urlpatterns = [
    path('adminPanel/', AdminCollegueView.as_view(), name='Admin'),
    path('viewProductsAdmin/', viewProductsAdmin.as_view(), name='ViewProductsAdmin'),
    path('deleteInvoice/<int:invoice_id>/', deleteAvoiceAdmin.as_view(), name='DeleteInvoice'),
    path('deleteProductsAdmin/<int:product_id>/', DeleteProductAdmin.as_view(), name='DeleteProductsAdmin'),
    path('view_all_companies/', viewAllCompaniesAdmin.as_view(), name='ViewAllCompanies'),
    path('delete_company/<int:company_id>/', deleteCompanyAdmin, name='DeleteCompany'),
    path('createSuperAdmin/', CreateSuperAdmin.as_view(), name='CreateSuperAdmin'),
    path('createCollegeAdmin/', CreateCollegesAdmin.as_view(), name='CreateCollegeAdmin'),
    path('deleteCollegeAdmin/', deleteCollegeAdmin, name='DeleteCollegeAdmin'),
    path('view_companies_for_college', CompaniesForCollegeAdmin.as_view(), name='ViewCompaniesForCollege')
]