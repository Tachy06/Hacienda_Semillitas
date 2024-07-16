from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from PageLogin.models import CustomUser
from django.contrib import messages
from datetime import date

# Create your views here.
class productsView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        year = date.today().year
        return render(request, 'products.html', {'year': year})
    def post(self, request):
        product = request.POST.get('product')
        description = request.POST.get('description')
        price = request.POST.get('price')
        user = CustomUser.objects.get(email=request.user)
        ProductsRegister.objects.create(user=user, name=product, description=description, price=price, college=user.college)
        return redirect('/products')
    
class searchForCollege(View):
    def get(self, request):
        year = date.today().year
        college = College.objects.all()
        return render(request, 'searchForCollege.html', {'year': year, 'colleges': college})
    def post(self, request):
        college = request.POST.get('college')
        return redirect(f'/view-products/{college}')
    
class ProductsView(View):
    def get(self, request, college_id):
        products = ProductsRegister.objects.filter(college=college_id)
        year = date.today().year
        return render(request, 'view-products.html', {'products': products, 'year': year})
    
class deleteProductsView(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        products = ProductsRegister.objects.filter(user=user)
        year = date.today().year
        return render(request, 'delete-products.html', {'products': products, 'year': year})
    
class deleteProducts(LoginRequiredMixin, View):
    login_url = '/'
    def post(self, request, product_id):
        product = get_object_or_404(ProductsRegister, id=product_id, user=request.user)
        product.delete()
        return redirect('/delete-products/')
    
class searchForModify(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        product = ProductsRegister.objects.filter(user=user)
        year = date.today().year
        return render(request, 'searchForModify.html', {'products': product, 'year': year})
    def post(self, request):
        product = request.POST.get('product')
        user = CustomUser.objects.get(email=request.user)
        productSearch = ProductsRegister.objects.get(user=user, id=product)
        return redirect(f'/modifyProduct/{productSearch.id}')
    
class ModifyProducts(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request, product_id):
        product = ProductsRegister.objects.get(id=product_id)
        year = date.today().year
        return render(request, 'modifyProducts.html', {'product': product, 'year': year})
    def post(self, request, product_id):
        product = get_object_or_404(ProductsRegister, id=product_id, user=request.user)
        productSearch =request.POST.get('product')
        description = request.POST.get('description')
        price = request.POST.get('price')
        if productSearch.isspace():
            messages.error(request, 'Ingresa un nombre de producto')
            return redirect(f'/modifyProduct/{product_id}')
        elif description.isspace():
            messages.error(request, 'Ingresa una descripción')
            return redirect(f'/modifyProduct/{product_id}')
        elif price.isspace():
            messages.error(request, 'Ingresa un precio')
            return redirect(f'/modifyProduct/{product_id}')
        product.name = productSearch
        product.description = description
        product.price = price
        product.save()
        return redirect('/')