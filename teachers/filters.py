from .models import Teacher
import django_filters


class TeacherFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = ['teacher_id']
