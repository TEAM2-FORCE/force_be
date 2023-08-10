from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Product, Market
from .serializers import ProductSerializer, MarketSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from rest_framework.generics import ListAPIView
from rest_framework.exceptions import NotFound


class ProductsList(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
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
        return products
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    
class ProductDetail(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(pd_id=id)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")

    def get(self, request, id):
        product = self.get_object(id)
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
    
class MarketList(APIView):
    # def post(self, request, id): # id 값을 가지는 게시물에 댓글 생성
    #     request.data["product"] = id
    #     serializer = MarketSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, id): # id 값을 가지는 게시물에 댓글 생성
        # request.data["product"] = id
        request_data_copy = request.data.copy() # mutable 한 딕셔너리로 카피하는 메서드
        request_data_copy['product'] = id
        serializer = MarketSerializer(data=request_data_copy)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id): # id 값을 가지는 게시물의 모든 댓글을 조회
        markets = Market.objects.filter(product=id)
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)