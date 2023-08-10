from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.generics import ListAPIView

class ProductsList(ListAPIView):
    def get(self, request, format=None):
        sort_std = self.request.query_params.get('sort', 'default')
        product_query = Product.objects.all()

        if sort_std == 'default':
            products = product_query.order_by('-pd_like_cnt')
        
        elif sort_std == 'name':
            products = product_query.order_by('pd_name')
        
        elif sort_std == 'price':
            products = product_query.order_by('pd_price')

        elif sort_std == '-price':
            products = product_query.order_by('-pd_price')
        else:
            products = product_query
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetail(APIView):
    def get_object(self, id):
        product = Product.objects.get(id=Product.pd_id)
        self.check_object_permissions(self.request, product)
        return product
    
    def get(self, request, id):
        product = Product.objects.get(pd_id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = Product.objects.get(pd_id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = Product.objects.get(pd_id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductCategory(APIView):
    def get(self, request, cg_id):
        sort_std = self.request.query_params.get('sort', 'default')
        product_query = Product.objects.filter(cg_id=cg_id)

        if sort_std == 'default':
            products = product_query.order_by('-pd_like_cnt')
        
        elif sort_std == 'name':
            products = product_query.order_by('pd_name')
        
        elif sort_std == 'price':
            products = product_query.order_by('pd_price')

        elif sort_std == '-price':
            products = product_query.order_by('-pd_price')
        else:
            products = product_query
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)