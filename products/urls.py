from django.urls import path
from products.views import *

urlpatterns = [
    path('', ProductsList.as_view()),
    path('<int:id>/', ProductDetail.as_view()),
    path('category/<int:cg_id>/', ProductCategory.as_view()),

    path('<int:id>/market/', MarketList.as_view()),

    path('<int:id>/vegan/', VeganList.as_view()),

    path('<int:id>/wish/', WishlistList.as_view()),
    path('wish/', WishlistList.as_view()),

    path('<int:id>/ingredients/', ProductIngredients.as_view()),
]