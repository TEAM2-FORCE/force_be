from django.urls import path
from .views import *

urlpatterns = [
    path('', IgdList.as_view(), name='ingredients_list'),
    path('<int:pk>/', IgdDetail.as_view(), name='ingredient_detail'),
]