from rest_framework import serializers
from .models import Ingredients

class IgdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredients
        fields = "__all__"
