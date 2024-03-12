from django.urls import path
from rest_framework.routers import DefaultRouter

from api.auth.views import RegisterView, UserAuthenticationView
from api.v1.books.views import BookModelViewSet


router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [
        # registration
        path("register/", RegisterView.as_view({"post": "register"}), name="register"),

        # login
        path("login/", UserAuthenticationView.as_view({"post": "login"}), name="login"),
        path("logout/", UserAuthenticationView.as_view({"post": "logout"}), name="logout"),

        # book
        path("book/", BookModelViewSet.as_view({"get": "list"}), name="book-list"),
        path("book/create/", BookModelViewSet.as_view({"post": "create"}), name="book-create"),
        path("book/<int:pk>", BookModelViewSet.as_view({"put": "update"}), name="book-update"),
        path("book/<int:pk>/", BookModelViewSet.as_view({"delete": "destroy"}), name="book-delete"),
    ]
)
