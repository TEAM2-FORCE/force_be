from django.urls import path
from .views import *
from .models import *

urlpatterns = [
    path('list/', IgdList.as_view(), name = 'ingredients_list'),
    path('<int:id>/', IgdDetail.as_view(), name = 'ingredient_detail'),
    
    path('<int:igd_id>/bm/', IgdBm.as_view(), name = 'ingredient_bookmark'),
    path('bm/', IgdBm.as_view(), name = 'ingredients_bookmark_list'),

    path('', IgdSearchListView.as_view(), name = 'ingredeint_search'),

    path('filter/', IgdFilterListView.as_view(), name = 'ingredeint_caution_list'),

    path('<int:id>/products/', IngredientProducts.as_view()),

    path('bookmarked/', BookmarkIngredient.as_view()),
]
