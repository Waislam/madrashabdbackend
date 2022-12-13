from .models import StudentIncome, OtherIncome, AllExpense
import django_filters


class StudentIncomeFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = StudentIncome
        fields = ['student']


class OtherIncomeFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = OtherIncome
        fields = ['receipt_book_number']


class AllExpenseFilter(django_filters.FilterSet):
    # user__phone = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = AllExpense
        fields = ['voucher_name']