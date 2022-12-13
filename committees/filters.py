from .models import Committee, PermanentMembers, OtherMembers
import django_filters


class CommitteeFilter(django_filters.FilterSet):
    class Meta:
        model = Committee
        fields = ['phone_number', 'member_name']


class PermanentMembersFilter(django_filters.FilterSet):
    class Meta:
        model = PermanentMembers
        fields = ['phone_number', 'member_name']


class OtherMembersFilter(django_filters.FilterSet):
    class Meta:
        model = OtherMembers
        fields = ['phone_number', 'member_name']