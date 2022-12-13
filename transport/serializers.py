from rest_framework import serializers
from .models import (
    VehicleInfo,
    TransportDetail,
)


class VehicleInfoListSerializers(serializers.ModelSerializer):
    class Meta:
        model = VehicleInfo
        fields = [
            'id',
            'madrasha',
            'car_number',
            'driver_name',
            'driver_number',
            'route',
            'start_time',
        ]

        depth = 2


class VehicleInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = VehicleInfo
        fields = [
            'id',
            'madrasha',
            'car_number',
            'driver_name',
            'driver_number',
            'route',
            'start_time',
        ]


class TransportDetailListSerializers(serializers.ModelSerializer):
    class Meta:
        model = TransportDetail
        fields = [
            'id',
            'madrasha',
            'student_id',
            'vehicle',
        ]

        depth = 2


class TransportDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = TransportDetail
        fields = [
            'id',
            'madrasha',
            'student_id',
            'vehicle',
        ]



