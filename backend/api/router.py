from django.urls import path
from rest_framework.routers import DefaultRouter

from api.v1.books.views import BookModelViewSet
from apps.chat.views import lobby
from api.auth.views import (
    RegisterView,
    UserAuthenticationView,
    GitHubSignInView
)

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [
        # registration
        path("register/", RegisterView.as_view(), name="register"),
        # registration GitHub
        path("github/", GitHubSignInView.as_view(), name="github-sign-in"),
        # chat lobby
        path("chat/", lobby, name="lobby"),


        # login
        path("login/", UserAuthenticationView.as_view(), name="login"),
        path("logout/", UserAuthenticationView.as_view(), name="logout"),

        # book
        path("book/", BookModelViewSet.as_view({"get": "list"}), name="book-list"),
        path("book/create/", BookModelViewSet.as_view({"post": "create"}), name="book-create"),
        path("book/<int:pk>", BookModelViewSet.as_view({"put": "update"}), name="book-update"),
        path("book/<int:pk>/", BookModelViewSet.as_view({"delete": "destroy"}), name="book-delete"),

        # book transfer
        path("book/<int:pk>/transfer/", BookModelViewSet.as_view({"post": "transfer"}), name="book-transfer"),
    ]
)


'''

Keneshbekov_

matoma44zz



'''
