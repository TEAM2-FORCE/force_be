from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import *
from .serializers import *


class IgdList(APIView):
    
    # 전체 성분 조회
    def get(self, request, format = None):
        igds = Ingredient.objects.all()
        serializer = IgdSerializer(igds, many = True) #다수 객체 이용
        return Response(serializer.data)

    # 성분 데이터 DB 저장
    def post(self, request, format = None):
        data = request.data
        serializer = IgdSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else : 
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
class IgdDetail(APIView):

    # 개별 성분 조회
    def get(self, request, id, format = None):
        igd = get_object_or_404(Ingredient, igd_id = id)
        serializer = IgdSerializer(igd)
        return Response(serializer.data)