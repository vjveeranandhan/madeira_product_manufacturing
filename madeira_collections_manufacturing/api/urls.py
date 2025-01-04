from django.urls import path
from user_manager.views import create_user, delete_user, login_view, get_all_users, get_user_by_id
from inventory.views import get_all_categories, create_category, get_category, update_category, delete_category
from inventory.views import get_all_materials, create_material, get_material, update_material, delete_material
from process.views import get_all_processes, create_process, update_process, delete_process, get_process

urlpatterns = [
    #user and Login api's
    path('users/login/', login_view, name='login'),
    path('create-user/', create_user, name='create_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/', get_all_users, name='get_all_user'),
    path('users/<int:user_id>/', get_user_by_id, name='get_user_by_id'),

    #inventory category api's
    path('categories/', get_all_categories, name='get_all_categories'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/<int:pk>/', get_category, name='get_category'),
    path('categories/<int:pk>/update/', update_category, name='update_category'),
    path('categories/<int:pk>/delete/', delete_category, name='delete_category'),

    #inventory material api's
    path('materials/', get_all_materials, name='get_all_materials'),
    path('materials/create/', create_material, name='create_material'),
    path('materials/<int:pk>/', get_material, name='get_material'),
    path('materials/<int:pk>/update/', update_material, name='update_material'),
    path('materials/<int:pk>/delete/', delete_material, name='delete_material'),

    #processes api's
    path('processes/', get_all_processes, name='get_all_processes'),
    path('processes/create/', create_process, name='create_process'),
    path('processes/<int:pk>/', get_process, name='get_process'),
    path('processes/<int:pk>/update/', update_process, name='update_process'),
    path('processes/<int:pk>/delete/', delete_process, name='delete_process'),

]