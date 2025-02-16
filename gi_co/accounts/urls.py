from django.urls import path
from .views import UserView


urlpatterns = [
    path('user-data/', UserView.as_view(), name='user_data'),
]