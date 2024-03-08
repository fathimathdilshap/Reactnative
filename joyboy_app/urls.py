from django.urls import path
from .api_views import *
from . import api_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='post-list'),
    path('post_categories/', PostCategoryListAPIView.as_view(), name='post-category-list'),
    path('booking/', BookingCreateAPIView.as_view(), name='book'),
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    path('userlogin/', LoginAPIView.as_view(), name='userlogin'),
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('logout/', LogoutAPIView.as_view(), name='user-logout'),
    path('check-auth/', CheckAuthAPIView.as_view(), name='check-auth'),
    path('booking_details/',Booking_detailsAPIView.as_view(),name='booking_details'),
    path('booking_details/<int:booking_id>/', Booking_detailsAPIView.as_view(), name='booking_details_delete'),
    path('change_password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('turf/', TurfAPIView.as_view(), name='turf-api'),
    path('turfs/', TurfListCreateView.as_view(), name='turf-list-create'),
    path('edit/', TurfRetrieveUpdateDestroyView.as_view(), name='Edit-Turf'),
    path('turfs/<int:pk>/', TurfRetrieveUpdateDestroyView.as_view(), name='turf-retrieve-update-destroy'),
    path('delete/',DeleteserviceAPIView.as_view(), name='deleteservice'),
    path('update_profile/', EditprofileAPIView.as_view(), name='updateprofile'),
    path('turfs/<int:id>/', TurfUpdateAPIView.as_view(), name='update-turf'),
    
]
