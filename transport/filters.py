from .models import VehicleInfo, TransportDetail
import django_filters


class VehicleInfoFilter(django_filters.FilterSet):
    class Meta:
        model = VehicleInfo
        fields = ['car_number', 'driver_name', 'driver_number']


class TransportDetailFilter(django_filters.FilterSet):
    class Meta:
        model = TransportDetail
        fields = ['vehicle__car_number']
