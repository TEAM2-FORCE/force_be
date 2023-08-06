from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import *
from .serializers import *


class IgdList(APIView):
    
    def get(self, request, format = None):
        igd = Ingredients.objects.all()
        serializer = IgdSerializer(igd, many = True) #다수 객체 이용
        return Response(serializer.data)

    def post(self, request, format = None):
        data = request.data
        serializer = IgdSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)