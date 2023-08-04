
from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=True)
router.register('', views.ProductViewSet, basename='prod'),

urlpatterns = [
    path('prod/', include(router.urls)),
]