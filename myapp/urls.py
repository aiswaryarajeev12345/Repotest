from django.urls import path
from . import views

urlpatterns = [

    # Home
    path(
        '',
        views.home,
        name='home'
    ),

    # User Registration
    path(
        'register/',
        views.register,
        name='register'
    ),

    # Login
    path(
        'login/',
        views.user_login,
        name='login'
    ),

    # Logout
    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    # User Dashboard
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # User Help Request
    path(
        'request-help/',
        views.request_help,
        name='request_help'
    ),

    # User My Requests
    path(
        'my-requests/',
        views.my_requests,
        name='my_requests'
    ),

    # Admin Dashboard
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    

    # Coordinator Dashboard
    path(
        'coordinator/',
        views.coordinator_dashboard,
        name='coordinator_dashboard'
    ),

    # Update Help Request
    path(
        'coordinator/update-request/<int:pk>/',
        views.update_help_request,
        name='update_help_request'
    ),

]