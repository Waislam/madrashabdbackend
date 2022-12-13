from . import models
import django_filters


class DistrictFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.District
        fields = ['division']


class PostOfficeFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.PostOffice
        fields = ['district']


class PostCodeFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.PostCode
        fields = ['post_office']


class ThanaFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Thana
        fields = ['district']
