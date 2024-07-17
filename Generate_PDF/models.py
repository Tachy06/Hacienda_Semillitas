from django.db import models
from PageLogin.models import *

# Create your models here.
class GenerateInvoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100, null=False)
    product = models.CharField(max_length=100, null=False)
    quantity = models.IntegerField(null=False)
    method_paid = models.CharField(max_length=100, null=False)
    total = models.FloatField(null=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.customer} - {self.date}'