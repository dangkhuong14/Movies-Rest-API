from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse
from watchlist_app.api.serializers import MovieSerializer

# Create your views here.


@api_view(['GET', 'POST'])
def movie_list(request):
    if (request.method == 'GET'):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    if (request.method == 'POST'):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_details(request, pk):
    if request.method == 'GET':
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    if request.method == 'PUT':
        movie = Movie.objects.get(pk=pk)
        # Serializer object biet duoc khi nao goi ham create() hay update() trong serializer class
        # bang cach kiem tra thuoc tinh instance chua Model instance co dang duoc serializer xu ly
        # cu the o day la movie variable
        serializer = MovieSerializer(movie, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    if request.method == 'DELETE':
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
