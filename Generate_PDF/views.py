from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from PageLogin.models import CustomUser
from PagePrincipal.models import ProductsRegister
from django.http import HttpResponse
from weasyprint import HTML
import datetime
# Create your views here.

class GeneratePDF(LoginRequiredMixin, View):
    login_url = '/'
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        products = ProductsRegister.objects.filter(user=user)
        return render(request, 'generate-pdf.html', {'products': products})
    def post(self, request):
        # Obtener los datos de la factura
        name_customer = request.POST.get('name')
        amount = request.POST.get('amount')
        product = request.POST.get('product')
        user = CustomUser.objects.get(email=request.user)
        items = ProductsRegister.objects.filter(id=product)
        product_name = ProductsRegister.objects.get(id=product).name
        subtotal = sum(item.price * float(amount) for item in items)
        service_charge = subtotal * 0.13
        total = subtotal + service_charge

        # Contexto para el template
        context = {
            'company': user.company_name,
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.datetime.now().strftime('%H:%M %p'),
            'identifier': name_customer,
            'seller': user.name_of_student,
            'items': items,
            'amount': amount,
            'subtotal': subtotal,
            'service_charge': service_charge,
            'total': total,
        }

        # Renderizar el HTML con el contexto
        html_string = render(request, 'commercial_invoice.html', context).content.decode('utf-8')

        # Crear el PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Guardar el PDF en la base de datos
        GenerateInvoice.objects.create(user=user, college=user.college, customer=name_customer, product=product_name, quantity=amount, total=total)

        # Responder con el PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Factura para {name_customer}.pdf"'

        return response