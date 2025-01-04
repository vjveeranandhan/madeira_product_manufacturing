from django.urls import path
from user_manager.views import create_user, delete_user, login_view, get_all_users, get_user_by_id
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/login/', login_view, name='login'),
    path('create-user/', create_user, name='create_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/', get_all_users, name='get_all_user'),
    path('users/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
]