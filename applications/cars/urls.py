from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.cars.views import CarClassView, CarView, TravelView, CommentView, FavoriteView

router = DefaultRouter()
router.register('carclass', CarClassView)
router.register('travel', TravelView)
router.register('comment', CommentView)
router.register('', CarView)


urlpatterns = [
    path('', include(router.urls)),
    ]