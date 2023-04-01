from django.shortcuts import render
from rest_framework import generics, permissions
from django.db.models import Q
from .models import House, Booking
from .serializers import HouseSerializer, BookingSerializer


class HouseList(generics.ListAPIView):
    serializer_class = HouseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query_params = self.request.query_params
        houses = House.objects.all()

        if 'date' in query_params and 'from' in query_params and 'to' in query_params and 'guests' in query_params:
            date = query_params.get('date')
            from_date = query_params.get('from')
            to_date = query_params.get('to')
            guests = int(query_params.get('guests'))

            bookings = Booking.objects.filter(
                Q(start_date__range=[from_date, to_date]) | Q(end_date__range=[from_date, to_date])
            )

            booked_houses = bookings.values_list('house_id', flat=True)
            houses = houses.exclude(id__in=booked_houses).filter(max_guests__gte=guests)

        return houses


class BookingCreate(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookingList(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)
