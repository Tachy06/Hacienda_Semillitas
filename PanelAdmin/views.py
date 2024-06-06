from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from PagePrincipal.models import ProductsRegister
from PageLogin.models import *
from Generate_PDF.models import *

# Create your views here.
class AdminCollegueView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        college = College.objects.get(name=user.college)
        invoices = GenerateInvoice.objects.filter(college=college)
        total = sum(float(product.total) for product in invoices)
        url = '/'
        return render(request, 'PanelAdmin.html', {'invoices': invoices, 'total': total, 'url': url})
    
class viewProductsAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        college = College.objects.get(name=user.college)
        products = ProductsRegister.objects.filter(college=college)
        url = '/adminPanel/'
        return render(request, 'viewProductsAdmin.html', {'products': products, 'url': url})
    
class deleteAvoiceAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, invoice_id):
        GenerateInvoice.objects.get(id=invoice_id).delete()
        return redirect('/adminPanel/')