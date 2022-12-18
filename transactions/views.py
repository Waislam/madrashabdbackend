from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from datetime import datetime, timedelta

from accounts.models import Madrasha
from students.models import Student, FessInfo
from .serializers import (IncomeCategorySerializer, IncomeSubCategorySerializer, StudentIncomeSerializer,
                          OtherIncomeSerializer,
                          OtherIncomeListSerializer, StudentIncomeListSerializer, AllExpenseListSerializer,
                          AllExpenseSerializer, ExpenseCategorySerializer, ExpenseSubCategorySerializer)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import (IncomeCategory,
                     IncomeSubCategory,
                     StudentIncome,
                     ExpenseCategory,
                     OtherIncome,
                     AllExpense,
                     ExpenseSubCategory
                     )
from django.http.response import JsonResponse
from rest_framework import mixins, generics, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import StudentIncomeFilter, OtherIncomeFilter, AllExpenseFilter
from students.pagination import CustomPagination
from django.contrib.auth import get_user_model

user = get_user_model()


# Create your views here.
class CategoryView(ListAPIView):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer


class SubCategoryList(APIView):
    def post(self, request):
        category = request.data['category']
        sub_cat = {}
        if category:
            sub_cats = IncomeCategory.objects.get(id=category).sub_categories.all()
            sub_cat = {d.name: d.id for d in sub_cats}
        return JsonResponse(data=sub_cat, safe=False)


class TransactionSubCategory(mixins.ListModelMixin,
                             generics.GenericAPIView):
    queryset = IncomeSubCategory.objects.all()
    serializer_class = IncomeSubCategorySerializer

    def get_queryset(self):
        """to get any parameter from api"""
        category = self.kwargs['category']
        return super().get_queryset().filter(
            category__pk=category
        )

    def get(self, request, *args, **kwargs):
        """method to show the list of Income from sub_category"""
        # self.serializer_class = StudentListSerializer
        return self.list(request, *args, **kwargs)


class ExpenseCategoryList(ListAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer


class ExpenseSubCategoryList(APIView):
    def post(self, request):
        category = request.data['category']
        sub_cat = {}
        if category:
            sub_cats = ExpenseCategory.objects.get(id=category).expense_sub_cats.all()
            sub_cat = {d.name: d.id for d in sub_cats}
        return JsonResponse(data=sub_cat, safe=False)


class TransactionExpenseSubCategory(mixins.ListModelMixin,
                                    generics.GenericAPIView):
    queryset = ExpenseSubCategory.objects.all()
    serializer_class = ExpenseSubCategorySerializer

    def get_queryset(self):
        """to get any parameter from api"""
        category = self.kwargs['category']
        return super().get_queryset().filter(
            category__pk=category
        )

    def get(self, request, *args, **kwargs):
        """method to show the list of Income from sub_category"""
        # self.serializer_class = StudentListSerializer
        return self.list(request, *args, **kwargs)


class StudentIncomeCreateView(APIView):
    """
    This view creating both studentincome at transaction and feesInfo at student model
    """
    def post(self, request, madrasha_slug, formate=None):
        """Method to create Income from student obj"""

        requested_data = request.data
        student = requested_data["student"]
        student_id = Student.objects.get(student_id=student).id
        requested_data["student"] = student_id

        madrasha_instance = Madrasha.objects.get(id=requested_data['madrasha'])
        created_by = user.objects.get(id=requested_data['created_by'])
        student_inactance = Student.objects.get(id=requested_data['student'])
        student_income = {
            "madrasha": requested_data["madrasha"],
            "student": requested_data["student"],
            "total_amount": requested_data["total_amount"],
            "paid_date": requested_data["paid_date"],
            "created_by": requested_data["created_by"]
        }
        st_income = StudentIncome(
            madrasha=madrasha_instance,
            student=student_inactance,
            total_amount=requested_data["total_amount"],
            paid_date=requested_data["paid_date"],
            created_by=created_by
        )
        st_income.save()
        # StudentIncome.objects.create(**student_income)
        student_income_id = StudentIncome.objects.all().last()
        fees = []
        for obj in requested_data['fees_detail']:
            date_format = "%Y-%m-%d"
            from_date = datetime.strptime(str(obj["from_date"]), date_format)
            to_date = datetime.strptime(str(obj["to_date"]), date_format)
            date_difference = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
            month_value = date_difference + 1
            print(month_value)
            if month_value == 1:
                obj['madrasha'] = madrasha_instance
                obj["student"] = student_inactance
                obj["student_income"] = student_income_id
                obj["paid_date"] = from_date
                FessInfo.objects.create(
                    madrasha=obj['madrasha'],
                    student=obj["student"],
                    student_income=obj["student_income"],
                    current_fee=obj["current_fee"],
                    fees_type=obj["fees_type"],
                    # fees_type_term=obj["fees_type_term"]
                    paid_date=obj["paid_date"],
                    paid_amount=obj["paid_amount"]
                )
            else:
                x = from_date
                full_year = x.year
                month = x.month
                days = x.day

                for each in range(month_value):
                    from_date = str(full_year) + "-" + str(month + each) + "-" + str(days)
                    obj['madrasha'] = madrasha_instance
                    obj["student"] = student_inactance
                    obj["student_income"] = student_income_id
                    obj["paid_date"] = from_date
                    FessInfo.objects.create(
                        madrasha=obj['madrasha'],
                        student=obj["student"],
                        student_income=obj["student_income"],
                        current_fee=obj["current_fee"],
                        fees_type=obj["fees_type"],
                        # fees_type_term=obj["fees_type_term"]
                        paid_date=obj["paid_date"],
                        paid_amount=obj["paid_amount"]
                    )
        return Response({"status": True, "message": "Operation has been done successfully"})


class StudentIncomeView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                        generics.GenericAPIView):
    queryset = StudentIncome.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = StudentIncomeFilter
    search_fields = ["student", ""]
    pagination_class = CustomPagination

    def get_queryset(self):
        """to get any parameter from api"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super().get_queryset().filter(
            madrasha__slug=madrasha_slug
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StudentIncomeListSerializer
        return StudentIncomeSerializer

    def get(self, request, *args, **kwargs):
        """method to show the list of Income from Student"""
        # self.serializer_class = StudentListSerializer
        return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     """Method to create Income from student obj"""
    #     requested_data = request.data
    #     student = requested_data["student"]
    #     student_id = Student.objects.get(student_id=student).id
    #     requested_data["student"] = student_id
    #
    #     madrasha_instance = Madrasha.objects.get(id=requested_data['madrasha'])
    #     created_by = user.objects.get(id=requested_data['user_id'])
    #     student_inactance = Student.objects.get(id=requested_data['student'])
    #     student_income = {
    #         "madrasha": requested_data["madrasha"],
    #         "student": requested_data["student"],
    #         "total_amount": requested_data["total_amount"],
    #         "paid_date": requested_data["paid_date"],
    #         "created_by": requested_data["user_id"]
    #     }
    #     st_income = StudentIncome(
    #         madrasha=madrasha_instance,
    #         student=student_inactance,
    #         total_amount=requested_data["total_amount"],
    #         paid_date=requested_data["paid_date"],
    #         created_by=created_by
    #     )
    #     st_income.save()
    #     # StudentIncome.objects.create(**student_income)
    #     student_income_id = StudentIncome.objects.all().last()
    #     fees = []
    #     for obj in requested_data['fees_detail']:
    #         date_format = "%Y-%m-%d"
    #         from_date = datetime.strptime(str(obj["from_date"]), date_format)
    #         to_date = datetime.strptime(str(obj["to_date"]), date_format)
    #         date_difference = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
    #         month_value = date_difference + 1
    #         print(month_value)
    #         if month_value == 1:
    #             obj['madrasha'] = madrasha_instance
    #             obj["student"] = student_inactance
    #             obj["student_income"] = student_income_id
    #             obj["paid_date"] = from_date
    #             FessInfo.objects.create(
    #                 madrasha=obj['madrasha'],
    #                 student=obj["student"],
    #                 student_income=obj["student_income"],
    #                 current_fee=obj["current_fee"],
    #                 fees_type=obj["fees_type"],
    #                 # fees_type_term=obj["fees_type_term"]
    #                 paid_date=obj["paid_date"],
    #                 paid_amount=obj["paid_amount"]
    #             )
    #         else:
    #             x = from_date
    #             full_year = x.year
    #             month = x.month
    #             days = x.day
    #
    #             for each in range(month_value):
    #                 from_date = str(full_year) + "-" + str(month + each) + "-" + str(days)
    #                 obj['madrasha'] = madrasha_instance
    #                 obj["student"] = student_inactance
    #                 obj["student_income"] = student_income_id
    #                 obj["paid_date"] = from_date
    #                 FessInfo.objects.create(
    #                     madrasha=obj['madrasha'],
    #                     student=obj["student"],
    #                     student_income=obj["student_income"],
    #                     current_fee=obj["current_fee"],
    #                     fees_type=obj["fees_type"],
    #                     # fees_type_term=obj["fees_type_term"]
    #                     paid_date=obj["paid_date"],
    #                     paid_amount=obj["paid_amount"]
    #                 )
    #     return Response("Something done")


class StudentIncomeDetailView(APIView):
    """this class is for CRUD"""

    def get_object(self, pk):
        """For getting single obj with slug field"""
        try:
            return StudentIncome.objects.get(id=pk)
        except StudentIncome.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """For getting single object details"""
        student_income = self.get_object(pk)
        serializer = StudentIncomeListSerializer(student_income)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        """update single obj details"""
        student_income = self.get_object(pk)
        serializer = StudentIncomeSerializer(student_income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Student Income has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {"status": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class OtherIncomeView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = OtherIncome.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OtherIncomeFilter
    search_fields = ["receipt_book_number"]
    pagination_class = CustomPagination

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        return super().get_queryset().filter(
            madrasha__slug=madrasha_slug
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OtherIncomeListSerializer
        return OtherIncomeSerializer

    def get(self, request, *args, **kwargs):
        """method to show the list of Income from Student"""
        # self.serializer_class = StudentListSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Income from student obj"""
        # self.serializer_class = StudentSerializer
        return self.create(request, *args, **kwargs)


class OtherIncomeDetailView(APIView):
    """this class is for CRUD"""

    def get_object(self, pk):
        """For getting single obj with slug field"""
        try:
            return OtherIncome.objects.get(id=pk)
        except OtherIncome.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """For getting single object details"""
        other_income = self.get_object(pk)
        serializer = OtherIncomeListSerializer(other_income)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        """update single obj details"""
        other_income = self.get_object(pk)
        serializer = OtherIncomeSerializer(other_income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Other Income has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {"status": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AllExpenseView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = AllExpense.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AllExpenseFilter
    search_fields = ["voucher_name"]
    pagination_class = CustomPagination

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super().get_queryset().filter(
            madrasha__slug=madrasha_slug
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AllExpenseListSerializer
        return AllExpenseSerializer

    def get(self, request, *args, **kwargs):
        """method to show the list of Income from Student"""
        # self.serializer_class = StudentListSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Income from student obj"""
        # self.serializer_class = StudentSerializer
        return self.create(request, *args, **kwargs)


class AllExpenseDetailView(APIView):
    """this class is for CRUD"""

    def get_object(self, pk):
        """For getting single obj with slug field"""
        try:
            return AllExpense.objects.get(id=pk)
        except AllExpense.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """For getting single object details"""
        all_expense = self.get_object(pk)
        serializer = AllExpenseListSerializer(all_expense)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        """update single obj details"""
        all_expense = self.get_object(pk)
        serializer = AllExpenseSerializer(all_expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Expense has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {"status": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
