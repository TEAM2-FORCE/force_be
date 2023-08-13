import django_filters
from .models import Ingredient

class IgdCautionFilter(django_filters.FilterSet):
    igd_caution = django_filters.BooleanFilter(field_name = 'igd_caution')

    class Meta : 
        model = Ingredient
        fields = ['igd_caution']