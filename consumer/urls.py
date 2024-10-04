from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('consumerlogin',LoginView.as_view(template_name='consumer/consumer_login.html'),name='consumerlogin'),
    path('consumer-signup',views.consumer_signup_view,name='consumer-signup'),

    path('consumer-dashboard',views.consumer_dashboard_view,name='consumer-dashboard'),
    path('consumer-profile',views.consumer_profile_view,name='consumer-profile'),
    path('search',views.search_view,name='search'),

    path('add-to-cart/<int:pk>',views.add_to_cart_view,name='add-to-cart'),
    path('cart',views.cart_view,name='cart'),
    path('remove-service-from-cart/<int:pk>',views.remove_service_from_cart,name='remove-service-from-cart'),
    
    path('consumer-address',views.consumer_address_view,name='consumer-address'),
    path('payment',views.payment_view,name='payment'),
    path('payment-success',views.payment_success_view,name='payment-success'),
    path('my-bookings',views.my_bookings_view,name='my-bookings'),
    path('delete-booking/<int:pk>',views.delete_booking_from_mybookings,name='delete-booking'),
]