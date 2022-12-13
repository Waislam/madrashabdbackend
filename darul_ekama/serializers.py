from rest_framework import serializers
from darul_ekama.models import SeatBooking, NigraniTable


class SeatBookingSerializer(serializers.ModelSerializer):
    # madrasha students  building floor room seat is_active created_at
    class Meta:
        model = SeatBooking
        fields = '__all__'


class SeatBookingListSerializer(serializers.ModelSerializer):
    # madrasha students  building floor room seat is_active created_at
    class Meta:
        model = SeatBooking
        fields = '__all__'
        depth = 2


class NigraniTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = NigraniTable
        fields = '__all__'


class NigraniTableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = NigraniTable
        fields = '__all__'
        depth = 2


