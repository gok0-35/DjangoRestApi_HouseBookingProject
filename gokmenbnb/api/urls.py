from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import HouseList, BookingCreate, BookingList

urlpatterns = format_suffix_patterns([
    path('houses/', HouseList.as_view(), name='house-list'),
    path('bookings/create/', BookingCreate.as_view(), name='booking-create'),
    path('bookings/', BookingList.as_view(), name='booking-list'),
])
