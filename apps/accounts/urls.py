
from .views import CustomRegisterView, UserAPIView
from django.urls import path
from rest_framework import routers
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', views.AuthViewSet, basename='auth'),
urlpatterns = router.urls

# urlpatterns = [
#     path('register/', CustomRegisterView.as_view()),
#     path('users/', UserAPIView.as_view())
# ]

# urlpatterns = [
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ] + router.urls