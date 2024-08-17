from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from datetime import date

# Create your views here.
class HomeView(View):
    def get(self, request):
        year = date.today().year
        return render(request, 'index.html', {'year': year})
    
class LoginView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        company = authenticate(request, email=email, password=password)
        if company is not None:
            login(request, company)
            messages.success(request, 'Login exitoso')
            return redirect('/')
        else:
            messages.error(request, 'Credenciales incorrectas')
            return redirect('/')
        

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        college = College.objects.all()
        url = '/'
        return render(request, 'register.html', {'colleges': college, 'url': url})
    def post(self, request):
        company = request.POST.get('company')
        email = request.POST.get('email')
        password = request.POST.get('password')
        college = request.POST.get('college')
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')

        full_name = f'{name} {last_name}'
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya existe')
            return redirect('/')
        else:
            colegio = College.objects.get(id=college)
            CustomUser.objects.create_user(email=email, password=password, company_name=company, college=colegio, name_of_student=full_name)
            user = authenticate(request, email=email, password=password)
            login(request, user)
            messages.success(request, 'Registrado exitosamente')
            return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')


def testLogin(request):
    return render(request, 'testLogin.html')