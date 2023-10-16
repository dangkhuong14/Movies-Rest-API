from django.shortcuts import render
from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from user_app import models
from rest_framework.authtoken.models import Token
from rest_framework import status


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        serializer_data = {}

        if serializer.is_valid():
            new_user = serializer.save()

            # print(new_user)
            # >> user5 (username (__str__))
            # print(serializer.data)
            # >> {'username': 'user5', 'email': 'user5@gmail.com'}

            serializer_data['response'] = 'Registration Successful!'
            serializer_data['username'] = new_user.username
            serializer_data['email'] = new_user.email

            token = Token.objects.get(user=new_user)
            serializer_data['token'] = token.key
        else:
            serializer_data = serializer.errors

    return Response(serializer_data)


@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
