from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
class College(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
    def create_adminColegio(self, email, password=None, **extra_fields):
        extra_fields.setdefault('adminCollege', True)
        if extra_fields.get('adminCollege') is not True:
            raise ValueError('El Admin debe tener adminCollege=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    company_name = models.CharField(max_length=30, null=False)
    name_of_student = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=False)
    adminCollege = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    