from django.urls import path
from .views import *

urlpatterns = [
    path('generate_pdf/', GeneratePDF.as_view(), name='Generate_pdf'),
]