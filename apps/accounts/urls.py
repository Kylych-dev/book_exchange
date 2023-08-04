
from django.urls import path
from rest_framework import routers
from rest_framework import permissions
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


app_name = 'accounts'


router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', views.AuthViewSet, basename='auth')


schema_view = get_schema_view(
    openapi.Info(
        title="Book_exchange",
        default_version='v1',
        description="API documentation for your Django Rest Framework project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = router.urls

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]











# router = routers.DefaultRouter(trailing_slash=False)
# router.register('api/auth', views.AuthViewSet, basename='auth'),
# urlpatterns = router.urls

# urlpatterns = [
#     path('register/', CustomRegisterView.as_view()),
#     path('users/', UserAPIView.as_view())
# ]

# urlpatterns = [
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ] + router.urls