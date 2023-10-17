from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsAdminOrReviewOwnerOrReadOnly
# from rest_framework.decorators import api_view
# from django.shortcuts import render
# from django.http import JsonResponse

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer


class ReviewList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    """
        Thay đổi thuộc tính queryset của GenericAPIView class
        Không thay đổi trực tiếp trên thuộc tính queryset của lớp GenericAPIView vì:
        Tập dữ liệu queryset này là cố định và không thay đổi theo yêu cầu của request.
        Do đó cần sử dụng hàm get_queryset() của lớp GenericAPIView. 
        Hàm get_queryset() sẽ được gọi mỗi khi có request đến viewset. Hàm này có thể được sử dụng để lấy tập dữ liệu
        tùy chỉnh dựa trên yêu cầu của request.
    """

    def get_queryset(self):
        pk_watch = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk_watch)


class ReviewCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    # Thêm thuộc tính queryset là vì trong class đang dùng filter() hoặc get() của model Review
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(watchlist=self.kwargs['pk'])

    # Hàm perform_create được gọi trong action method của mixins.CreateModelMixin class
    def perform_create(self, serializer):
        pk_watch = self.kwargs['pk']
        watch_instance = WatchList.objects.get(pk=pk_watch)

        # Kiem tra User hien tai co tao review doi voi movie nay chua
        current_user = self.request.user
        review_queryset = Review.objects.filter(
            review_user=current_user, watchlist=watch_instance)

        if review_queryset.exists():
            raise ValidationError(
                "You've already reviewed this watching content")

        # Tinh toan lai rating cho watchlist sau khi review moi duoc them vao
        if watch_instance.num_ratings == 0:
            watch_instance.avg_rating = serializer.validated_data['rating']
        else:
            # Can sua lai logic
            watch_instance.avg_rating = (
                watch_instance.avg_rating + serializer.validated_data['rating'])/2

        watch_instance.num_ratings += 1
        watch_instance.save()

        # Any additional keyword arguments will be included in
        # the validated_data argument when .create() or .update() (method of serializers.Serialize class) are called.
        serializer.save(watchlist=watch_instance, review_user=current_user)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReviewOwnerOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


"""
            viewsets.ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet(ViewSetMixin, generics.GenericAPIView)) sử dụng actions của mixins mapping thành method handlers
"""


class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

# class viewsets.ViewSet(ViewSetMixin, views.APIView) chỉ mapping method -> action (Post->create)
# Khai báo hàm action mapping-> thành khai báo method

# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         platform = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(platform)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response('This watching content is not found',
                            status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        try:
            platforms = StreamPlatform.objects.all()
        except StreamPlatform.DoesNotExist:
            return Response('Can not found any streaming platforms',
                            status=status.HTTP_204_NO_CONTENT)

        serializer = StreamPlatformSerializer(
            platforms, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response('Streaming platform not found', status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(
            platform, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if (request.method == 'GET'):
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     if (request.method == 'POST'):
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'},
#                             status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         # Serializer object biet duoc khi nao goi ham create() hay update() trong serializer class
#         # bang cach kiem tra thuoc tinh instance chua Model instance co dang duoc serializer xu ly
#         # cu the o day la movie variable
#         serializer = MovieSerializer(movie, request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
