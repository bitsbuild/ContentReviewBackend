from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user.views import create_account,delete_account
urlpatterns = [
    path('create/',create_account,name='create'),
    path('token/',obtain_auth_token,name='token'),
    path('delete/',delete_account,name='delete')
]