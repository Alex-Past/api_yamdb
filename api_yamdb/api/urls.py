from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                       ReviewViewSet, CommentViewSet)

app_name = 'api'

router_v_1 = DefaultRouter()
router_v_1.register(r'titles', TitleViewSet, basename='titles')
router_v_1.register(r'genres', GenreViewSet, basename='genres')
router_v_1.register(r'categories', CategoryViewSet, basename='categories')
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


urlpatterns = [
    path('v1/', include(router_v_1.urls)),
]
