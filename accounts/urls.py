from django.urls import path, include
from .views import SignUp

urlpatterns = [
    path('', include('allauth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
]
