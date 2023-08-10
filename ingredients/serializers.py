from rest_framework import serializers
from .models import *

class IgdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = "__all__"

class IgdBmSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bookmark
        fields = "__all__"