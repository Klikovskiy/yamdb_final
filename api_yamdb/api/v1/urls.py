from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

app_name = 'api'

router = SimpleRouter()

router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns_auth = [
    path('signup/', APISignup.as_view(), name='signup'),
    path('token/', APIGetToken.as_view(), name='get_token')
]

urlpatterns = [
    path('auth/', include(urlpatterns_auth)),
    path('', include(router.urls)),
]
