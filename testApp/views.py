
from django.shortcuts import render
from drf_yasg import openapi
import requests
from bs4 import BeautifulSoup
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
                'texte': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DOUBLE),
            },
            required=['texte']
        ),
        responses={201: "Load Success", 400: "Bad Request"},
        operation_description=" Get Word"
    )
    def post(self, request):
        texte = ""
        try:
            texte = request.data.get('texte')
        except :
            return Response(status=status.HTTP_404_NOT_FOUND)
        #key = ""
        #url = f"https://pixabay.com/api?key={key}&q={texte}&image_type=photo"
        #response = requests.get(url)
        #data = response.json()
        #images = [result['webformatURL'] for result in data['hits']]
        images = chercher_liens_images(texte)

        return Response(images, status=status.HTTP_200_OK)








def chercher_liens_images(texte):
    recherche = texte.replace(' ', '+')
    url = f"https://www.google.com/search?q={recherche}&tbm=isch"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    balises_images = soup.find_all('img')
    liens_images = [balise['src'] for balise in balises_images if 'src' in balise.attrs]

    return liens_images