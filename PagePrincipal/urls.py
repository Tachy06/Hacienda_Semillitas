from django.urls import path
from .views import *

urlpatterns = [
    path('products/', productsView.as_view(), name='Products'),
    path('view-products/', ProductsView.as_view(), name='View-products'),
]