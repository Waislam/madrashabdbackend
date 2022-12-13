from django.contrib import admin
from .models import Committee, PermanentMembers, OtherMembers
# Register your models here.


class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['member_name', 'phone_number']
    search_fields = ['phone_number']
    list_per_page = 20

    class Meta:
        model = Committee


admin.site.register(Committee, CommitteeAdmin)


class PermanentMembersAdmin(admin.ModelAdmin):
    list_display = ['member_name', 'phone_number']
    search_fields = ['phone_number']
    list_per_page = 20

    class Meta:
        model = PermanentMembers


admin.site.register(PermanentMembers, PermanentMembersAdmin)


class OtherMembersAdmin(admin.ModelAdmin):
    list_display = ['member_name', 'phone_number']
    search_fields = ['phone_number']
    list_per_page = 20

    class Meta:
        model = OtherMembers


admin.site.register(OtherMembers, OtherMembersAdmin)