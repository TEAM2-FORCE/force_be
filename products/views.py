from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Products
from .serializers import ProductsSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

class ProductsList(APIView):
    def get(self, request, format=None):
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True) # 많은 값을 가져올 때는 다중값인 'many'를 True로 한다. 
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductsSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    