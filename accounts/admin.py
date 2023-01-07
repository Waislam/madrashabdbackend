from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(Address)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('division', 'district', 'thana', 'post_office', 'post_code')

    class Media:
        js = ("./js/dependable_dropdown_address_ajax.js",)


admin.site.register(Division)
admin.site.register(District)
admin.site.register(Thana)
admin.site.register(PostOffice)
admin.site.register(PostCode)


admin.site.register(Role)

# admin.site.register(CustomUser)
admin.site.register(User)


@admin.register(Madrasha)
class MadrashaModel(admin.ModelAdmin):
    list_display = ('name', 'madrasha_code', 'madrasha_address', 'madrasha_logo', 'created_at', 'updated_at', 'created_by', 'updated_by', 'active_status')


@admin.register(MadrashaUserListing)
class MadrashaUserListAdmin(admin.ModelAdmin):
    list_display = ('user', 'madrasha')



# @admin.register(Address)
# class AddressModel()
