from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from PageLogin.models import CustomUser
from PagePrincipal.models import ProductsRegister
from django.http import HttpResponse
from weasyprint import HTML
from datetime import date
import datetime
# Create your views here.

class GeneratePDF(LoginRequiredMixin, View):
    login_url = '/'
    
    def get(self, request):
        user = CustomUser.objects.get(email=request.user)
        year = date.today().year
        products = ProductsRegister.objects.filter(user=user)
        return render(request, 'generate-pdf.html', {'products': products, 'year': year})
    
    def post(self, request):
        # Obtener los datos de la factura
        name_customer = request.POST.get('name')
        user = CustomUser.objects.get(email=request.user)
        product_ids = request.POST.getlist('products')
        payment_method = request.POST.get('payment_method')
        
        items = []
        subtotal = 0

        for product_id in product_ids:
            quantity = request.POST.get(f'quantity-{product_id}')
            if quantity and int(quantity) > 0:
                product = ProductsRegister.objects.get(id=product_id)
                item_total = product.price * int(quantity)
                subtotal += item_total
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
        
        total = subtotal

        # Contexto para el template
        context = {
            'company': user.company_name,
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.datetime.now().strftime('%H:%M %p'),
            'identifier': name_customer,
            'seller': user.name_of_student,
            'items': items,
            'subtotal': subtotal,
            'payment_method': payment_method,
            'total': total,
        }

        # Renderizar el HTML con el contexto
        html_string = render(request, 'commercial_invoice.html', context).content.decode('utf-8')

        # Crear el PDF
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        # Guardar el PDF en la base de datos
        for item in items:
            GenerateInvoice.objects.create(
                user=user, 
                college=user.college, 
                customer=name_customer, 
                product=item['product'].name, 
                quantity=item['quantity'], 
                method_paid=payment_method,
                total=item['total']
            )

        # Responder con el PDF
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Factura_para_{name_customer}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response