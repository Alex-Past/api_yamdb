from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet

app_name = 'api'

router_v_1 = DefaultRouter()
router_v_1.register(r'titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router_v_1.urls)),
]
