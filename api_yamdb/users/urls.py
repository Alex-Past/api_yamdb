from django.urls import path

from api.views import get_token, signup

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='get_token'),
]
