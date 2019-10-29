from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EchoView(APIView):
    def post(self, request, *args, **kwarg):
        serializer = EchoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class UserDataView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserDataSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
