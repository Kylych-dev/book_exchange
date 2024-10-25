from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.chat.views import lobby
from api.v1.books.views import (
    BookModelViewSet,
    BooksByAuthorView
)
from api.auth.views import (
    RegisterView,
    UserAuthenticationView,
)

from api.v1.books.views import BookModelViewSet

from api.v1.author.views import (
    AuthorViewSet,
    GenreViewSet
)



router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [
        # registration
        path("register/", RegisterView.as_view(), name="register"),

        # login
        path("login/", UserAuthenticationView.as_view(), name="login"),
        path("logout/", UserAuthenticationView.as_view(), name="logout"),

        # book
        path("book/", BookModelViewSet.as_view({"get": "list"}), name="book-list"),
        path("book/create/", BookModelViewSet.as_view({"post": "create"}), name="book-create"),

        path("book/<int:pk>", BookModelViewSet.as_view(
            {
                'put': 'update',
                'get': 'retrieve',
                'delete': 'destroy'
            }
        ),
             name="book-detail"
        ),

        # path("book/<int:pk>", BookModelViewSet.as_view({"put": "update"}), name="book-update"),
        # path("book/<int:pk>/", BookModelViewSet.as_view({"delete": "destroy"}), name="book-delete"),

        # book transfer
        path("book/<int:pk>/transfer/", BookModelViewSet.as_view({"post": "transfer"}), name="book-transfer"),

        # author
        path("author/", AuthorViewSet.as_view({"get": "list"}), name="author-list"),

        # genre
        path("genre/", GenreViewSet.as_view({"get": "list"}), name="genre-list"),
        path('book/author/<int:author_id>/', BooksByAuthorView.as_view(), name='book-author'),
    ]
)