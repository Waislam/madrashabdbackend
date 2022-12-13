from .models import Student
import django_filters


class StudentFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['student_id']