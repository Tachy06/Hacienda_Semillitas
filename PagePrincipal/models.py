from django.db import models
from PageLogin.models import *

# Create your models here.
class ProductsRegister(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE)