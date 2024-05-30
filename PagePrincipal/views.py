from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from PageLogin.models import CustomUser

# Create your views here.
class productsView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        return render(request, 'products.html')
    def post(self, request):
        product = request.POST.get('product')
        description = request.POST.get('description')
        price = request.POST.get('price')
        user = CustomUser.objects.get(email=request.user)
        ProductsRegister.objects.create(user=user, name=product, description=description, price=price)
        return redirect('/products')
    
class ProductsView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        products = ProductsRegister.objects.all()
        return render(request, 'view-products.html', {'products': products})