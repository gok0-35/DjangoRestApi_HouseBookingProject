from django.shortcuts import render
from rest_framework import generics, permissions, pagination
from django.db.models import Q
from .models import House, Booking
from .serializers import HouseSerializer, BookingSerializer


class HouseList(generics.ListAPIView):
    serializer_class = HouseSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        query_params = self.request.query_params
        houses = House.objects.all()

        if 'date' in query_params and 'from' in query_params and 'to' in query_params and 'guests' in query_params and 'city' in query_params:
            date = query_params.get('date')
            from_date = query_params.get('from')
            to_date = query_params.get('to')
            guests = int(query_params.get('guests'))
            city = query_params.get('city')

            bookings = Booking.objects.filter(
                Q(start_date__range=[from_date, to_date]) | Q(end_date__range=[from_date, to_date])
            )

            booked_houses = bookings.values_list('house_id', flat=True)
            houses = houses.exclude(id__in=booked_houses).filter(max_guests__gte=guests, city__icontains=city)

        return houses 


class BookingCreate(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
        

class BookingList(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)
