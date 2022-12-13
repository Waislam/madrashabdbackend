from django.contrib import admin
from .models import VehicleInfo, TransportDetail


class VehicleInfoAdmin(admin.ModelAdmin):
    list_display = ['car_number', 'driver_name', 'driver_number']
    search_fields = ['car_number', 'driver_name', 'driver_number']
    list_per_page = 20

    class Meta:
        model = VehicleInfo


admin.site.register(VehicleInfo, VehicleInfoAdmin)


class TransportDetailAdmin(admin.ModelAdmin):
    list_display = ['vehicle']
    search_fields = ['vehicle']
    list_per_page = 20

    class Meta:
        model = TransportDetail


admin.site.register(TransportDetail, TransportDetailAdmin)