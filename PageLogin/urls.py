from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='Register'),
    path('logout/', logout_view, name='logout'),
    path('testLogin/', testLogin, name='testLogin'),
]