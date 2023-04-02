from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import HouseList, BookingCreate, BookingList

app_name = 'api'

urlpatterns = format_suffix_patterns([
    path('<str:version>/houses/', HouseList.as_view(), name='house-list'),
    path('<str:version>/bookings/create/', BookingCreate.as_view(), name='booking-create'),
    path('<str:version>/bookings/', BookingList.as_view(), name='booking-list'),
])