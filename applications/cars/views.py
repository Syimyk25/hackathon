from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from applications.cars.models import CarClass, Car, Travel, Rating, Like, Favorite, Comment
from applications.cars.permission import CustomIsAdmin
from applications.cars.serializers import CarClassSerializer, CarSerializer, TravelSerializer, CommentSerializer, \
    RatingSerializer, FavoriteSerializer


class CarPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10000


class TravelPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000

class TravelView(ModelViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer
    pagination_class = TravelPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        try:
            like_object, _ = Like.objects.get_or_create(owner=request.user, travel_id=pk)
            like_object.like = not like_object.like
            like_object.save()
            status = 'liked'

            if like_object.like:
                return Response({'status': status})
            status = 'unliked'
            return Response({'status': status})
        except:
            return Response('Нет такого объявления!')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [IsAuthenticated]
        elif self.action == 'like':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]



class CarClassView(ModelViewSet):
    queryset = CarClass.objects.all()
    serializer_class = CarClassSerializer
    pagination_class = CarPagination
    permission_classes = [CustomIsAdmin]


class CarView(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CarPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['owner']
    ordering_fields = ['id']
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        serializers = RatingSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(cars_id=pk, owner=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=201)

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):

        try:
            fav_obj, _ = Favorite.objects.get_or_create(owner=request.user, car_id=pk)
            fav_obj.favorite = not fav_obj.favorite
            fav_obj.save()
            status = 'favorite'
            if fav_obj.favorite:
                return Response({'status': status})
            status = 'not favorite'
            return Response({'status': status})
        except:
            return Response('Нет такого транспорта')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [IsAuthenticated]
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FavoriteView(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]