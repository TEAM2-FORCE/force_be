from django.urls import path
from products.views import *

urlpatterns = [
    path('', ProductsList.as_view()),
    path('<int:id>/', ProductDetail.as_view()),
    path('category/<int:cg_id>/', ProductCategory.as_view()),
]