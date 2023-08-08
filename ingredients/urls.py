from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path('', IgdList.as_view(), name = 'ingredients_list'),
    path('<int:id>/', IgdDetail.as_view(), name = 'ingredient_detail'),
    
    path('<int:igd_id>/bm/', IgdBm.as_view(), name = 'ingredient_bookmark'),
    path('bm/', IgdBm.as_view(), name = 'ingredients_bookmark_list'),
]