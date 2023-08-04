from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=True)
router.register('from/', views.RatingViewSet, basename='prod'),
for i in router:
    print(i)

urlpatterns = [
    path('from/', include(router.urls)),
]