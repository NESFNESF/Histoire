
from django.shortcuts import render
from drf_yasg import openapi
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
# Create your views here.



class  GetWordToPicture(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phrase': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DOUBLE),
            },
            required=['phrase']
        ),
        responses={201: "Load Success", 400: "Bad Request"},
        operation_description=" Get Word"
    )
    def post(self, request):
        phrase = ""
        try:
            phrase = request.data.get('phrase')
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)
        key = ""
        url = f"https://pixabay.com/api?key={key}&q={phrase}&image_type=photo"
        response = requests.get(url)
        data = response.json()
        images = [result['webformatURL'] for result in data['hits']]

        return Response(images, status=status.HTTP_200_OK)