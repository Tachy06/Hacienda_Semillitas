from django.urls import path
from .views import *

urlpatterns = [
    path('products/', productsView.as_view(), name='Products'),
    path('view-products/', ProductsView.as_view(), name='View-products'),
    path('delete-products/', deleteProductsView.as_view(), name='Delete-products'),
    path('delete-products/<int:product_id>/', deleteProducts.as_view(), name='Delete-product'),
    path('search/', searchForModify.as_view(), name='Search'),
    path('modifyProduct/<int:product_id>/', ModifyProducts.as_view(), name='Modify-product'),
]