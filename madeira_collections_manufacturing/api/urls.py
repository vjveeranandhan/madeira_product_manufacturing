from django.urls import path
from user_manager.views import create_user, delete_user, login_view, get_all_users, get_user_by_id, update_user_by_id
from inventory.views import get_all_categories, create_category, get_category, update_category, delete_category
from inventory.views import get_all_materials, create_material, get_material, update_material, delete_material
from process.views import get_all_processes, create_process, update_process, delete_process, get_process
from order.views import list_orders, create_order, retrieve_order, update_order, delete_order
from django.conf import settings
from django.conf.urls.static import static
from carpenter_work.views import list_carpenter_requests, carpenter_request_accept, carpenter_request_respond, carpenter_request_material_creation
from process.views import create_process_details, list_process_details, get_process_details, accept_process_details, delete_process_details
from process.views import create_process_material, retrieve_process_material, update_process_material, delete_process_material

# , retrieve_process_details,
urlpatterns = [
    #user and Login api's
    path('users/login/', login_view, name='login'),
    path('create-user/', create_user, name='create_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    path('users/', get_all_users, name='get_all_user'),
    path('users/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('users/<int:user_id>/update/', update_user_by_id, name='update_user_by_id'),

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

    #order api's
    path('orders/', list_orders, name='list_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/<int:pk>/', retrieve_order, name='retrieve_order'),
    path('orders/<int:pk>/update/', update_order, name='update_order'),
    path('orders/<int:pk>/delete/', delete_order, name='delete_order'),

    path('carpenter_requests/<int:carpenter_id>/', list_carpenter_requests, name='get_carpenter_requests'),
    path('carpenter_requests/<int:order_id>/<int:carpenter_id>/accept/',
         carpenter_request_accept, name='accept_carpenter_request'),
    path('carpenter_requests/<int:order_id>/<int:carpenter_id>/respond/',
         carpenter_request_respond, name='accept_carpenter_request'),
    path('carpenter_requests/<int:order_id>/<int:carpenter_id>/<int:carpenter_request_id>/<int:material_id>/create/',
         carpenter_request_material_creation, name='accept_carpenter_request'),
    # path('carpenter_request/<int:order_id>/delete/', carpenter_requests_delete, name='carpenter_requests_delete'),


    # path('process-details/', list_process_details, name='process-details-list'),
    path('process-details/create/', create_process_details, name='process-details-create'),
    # path('process-details/<int:process_details_id>/', retrieve_process_details, name='process-details-retrieve'),
    path('process-details/<int:process_manager_id>/<int:process_id>/', list_process_details, name='list-process-details-retrieve'),
    path('process-details/<int:process_manager_id>/<int:process_id>/<int:order_id>/', get_process_details, name='get-process-details'),
    path('process-details/<int:process_manager_id>/<int:process_id>/<int:order_id>/accept/', accept_process_details, name='accept-process-details'),
    path('process-details/<int:id>/delete/', delete_process_details, name='delete_process_details'),
    # path('process-details/<int:pk>/update/', update_process_details, name='process-details-update'),
    # path('process-details/<int:pk>/delete/', delete_process_details, name='process-details-delete'),

    path('process-materials/create/', create_process_material, name='create_process_material'),
    path('process-materials/<int:process_material_id>/', retrieve_process_material, name='retrieve_process_material'),
    path('process-materials/update/<int:process_material_id>/', update_process_material, name='update_process_material'),
    path('process-materials/delete/<int:process_material_id>/', delete_process_material, name='delete_process_material'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

