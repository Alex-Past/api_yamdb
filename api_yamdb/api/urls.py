from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                       ReviewViewSet, CommentViewSet, UserViewSet,
                       get_token, signup)

app_name = 'api'

router_v_1 = DefaultRouter()
router_v_1.register('titles', TitleViewSet, basename='titles')
router_v_1.register('genres', GenreViewSet, basename='genres')
router_v_1.register('categories', CategoryViewSet, basename='categories')
router_v_1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v_1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v_1.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='get_token'),
]
