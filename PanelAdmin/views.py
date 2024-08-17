from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from PagePrincipal.models import ProductsRegister
from PageLogin.models import *
from Generate_PDF.models import *
from django.contrib import messages

# Create your views here.
class AdminCollegueView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        if request.user.adminCollege:
            user = CustomUser.objects.get(email=request.user)
            college = College.objects.get(name=user.college)
            invoices = GenerateInvoice.objects.filter(college=college)
            total = sum(float(product.total) for product in invoices)
            url = '/'
            return render(request, 'PanelAdmin.html', {'invoices': invoices, 'total': total, 'url': url})
        elif request.user.is_superuser:
            user = CustomUser.objects.get(email=request.user)
            invoices = GenerateInvoice.objects.all()
            total = sum(float(product.total) for product in invoices)
            url = '/'
            return render(request, 'PanelAdmin.html', {'invoices': invoices, 'total': total, 'url': url})
    
class viewProductsAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        if request.user.adminCollege:
            user = CustomUser.objects.get(email=request.user)
            college = College.objects.get(name=user.college)
            products = ProductsRegister.objects.filter(college=college)
            url = '/adminPanel/'
            return render(request, 'viewProductsAdmin.html', {'products': products, 'url': url})
        elif request.user.is_superuser:
            user = CustomUser.objects.get(email=request.user)
            products = ProductsRegister.objects.all()
            url = '/adminPanel/'
            return render(request, 'viewProductsAdmin.html', {'products': products, 'url': url})
    
class deleteAvoiceAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, invoice_id):
        GenerateInvoice.objects.get(id=invoice_id).delete()
        messages.success(request, 'Factura eliminada exitosamente')
        return redirect('/adminPanel/')
    
class DeleteProductAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request, product_id):
        ProductsRegister.objects.get(id=product_id).delete()
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('/adminPanel/')
    
class viewAllCompaniesAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        if request.user.adminCollege:
            user = CustomUser.objects.get(email=request.user)
            companies = CustomUser.objects.filter(college=user.college)
            url = '/adminPanel/'
            return render(request, 'viewAllCompaniesAdmin.html', {'companies': companies, 'url': url})
        elif request.user.is_superuser:
            companies = CustomUser.objects.all()
            url = '/adminPanel/'
            return render(request, 'viewAllCompaniesAdmin.html', {'companies': companies, 'url': url})
        
def deleteCompanyAdmin(request, company_id):
    CustomUser.objects.get(id=company_id).delete()
    messages.success(request, 'Compañia o admin eliminado exitosamente')
    return redirect('/view_all_companies/')
        
class CreateSuperAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        url = '/adminPanel/'
        colleges = College.objects.all()
        return render(request, 'createSuperAdmin.html', {'url': url, 'colleges':colleges})
    def post(self, request):
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        college = request.POST.get('college')
        isAdmin = request.POST.get('RadioAdmin')
        password = request.POST.get('password')
        college_name = College.objects.get(id=college)
        try:
            user = CustomUser.objects.get(email=email)
            messages.error(request, 'El correo ya existe')
            return redirect('/adminPanel/')
        except CustomUser.DoesNotExist:
            if isAdmin == "Si":
                CustomUser.objects.create_superuser(email=email, password=password, company_name=f'{name} {last_name}', name_of_student=f'{name} {last_name}', college=College.objects.get(id=college))
                messages.success(request, 'Super Administrador creado exitosamente')
                return redirect('/adminPanel/')
            else:
                CustomUser.objects.create_adminColegio(email=email, password=password, company_name=f'{name} {last_name}', name_of_student=f'{name} {last_name}', college=College.objects.get(id=college))
                messages.success(request, f'Administrador del colegio {college_name} creado exitosamente')
                return redirect('/adminPanel/')
            
class CreateCollegesAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        url = '/adminPanel/'
        colleges = College.objects.all()
        return render(request, 'createColleges.html', {'url': url, 'colleges':colleges})
    def post(self, request):
        name = request.POST.get('name')
        try:
            college = College.objects.get(name=name)
            messages.error(request, 'El colegio ya existe')
            return redirect('/adminPanel/')
        except College.DoesNotExist:
            College.objects.create(name=name)
            messages.success(request, 'Colegio creado exitosamente')
            return redirect('/adminPanel/')
        
def deleteCollegeAdmin(request):
    college_id = request.POST.get('college_id')
    College.objects.get(id=college_id).delete()
    messages.success(request, 'Colegio eliminado exitosamente')
    return redirect('/adminPanel/')

class CompaniesForCollegeAdmin(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        if request.user.adminCollege:
            user = CustomUser.objects.get(email=request.user)
            companies = CustomUser.objects.filter(college=user.college)
            college = College.objects.get(name=user.college)
            url = '/adminPanel/'
            return render(request, 'ViewCompaniesForCollege.html', {'companies': companies, 'url': url, 'college': college})