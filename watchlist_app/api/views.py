from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from watchlist_app.models import Movie
from django.http import JsonResponse
from watchlist_app.api.serializers import MovieSerializer

# Create your views here.


@api_view()
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view()
def movie_details(request, pk):
    movie = Movie.objects.get(pk=pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

# def movie_list(request):
#     movies = Movie.objects.all()
#     # print(list(movies.values()))
#     data = {'movies': list(movies.values())}
#     return JsonResponse(data)

# def movie_details(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     data = {'name': movie.name,
#             'description': movie.description, 'active': movie.active}
#     return JsonResponse(data)
