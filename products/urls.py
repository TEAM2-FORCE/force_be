from django.urls import path
from products.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
]