from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from datetime import datetime, timedelta
from enum import Enum
from accounts.models import Madrasha
from students.models import Student, FessInfo
from settingapp.models import Fees
from students.serializers import FessInfoSerializer
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
import requests
from django.db.models import Count,Sum
from django.forms.models import model_to_dict

user = get_user_model()


class FeesType(Enum):
    ADMISSION = "ADMISSION"
    MONTHLY_TUITION = "MONTHLY_TUITION"
    BOARDING = "BOARDING"
    EXAMINATION = "EXAMINATION"
    TRANSPORT = "TRANSPORT"

class ExamTerm(Enum):
    FIRST_TERM = "FIRST_TERM"
    SECOND_TERM = "SECOND_TERM"
    THIRD_TERM = "THIRD_TERM"

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


def GetStudentIncomeUnpaid(student, madrasha, fees_type):
    madrasha_instance = Madrasha.objects.get(id=madrasha)
    student_inactance = Student.objects.get(id=student)
    student_id = Student.objects.get(id=student).id

    monthly_tution_fee = student_inactance.monthly_tution_fee
    academic_fee = student_inactance.academic_fees
    boarding_fee = student_inactance.boarding_feee
    admission_fee = student_inactance.admission_fee
    transport_fee = student_inactance.transport_fee
    tution_fee_active_from = str(student_inactance.tution_fee_active_from)
    boarding_fee_active_from = str(student_inactance.boarding_fee_active_from)
    transport_fee_active_from = str(student_inactance.transport_fee_active_from)

    is_tution_fee_active = student_inactance.is_tution_fee
    is_boarding_fee_active = student_inactance.is_boarding_fee
    is_transport_fee_active = student_inactance.is_transport_fee


    today = datetime.now()

    if (fees_type == FeesType.ADMISSION.value):
        total_due = 0
        get_admission_fees = FessInfo.objects.filter(student=student_id, fees_type=fees_type,
                                                     paid_date__year=today.strftime("%Y"))
        print(get_admission_fees)
        if not get_admission_fees:
            total_due = student_inactance.admission_fee

        return ({"status": 200, "fees_type": fees_type, "total_amount": total_due})

    elif (fees_type == FeesType.EXAMINATION.value):
        current_date = datetime.strptime(today.strftime("%Y-%m-%d"), "%Y-%m-%d")
        student_class=student_inactance.admitted_class.id
        term_fees = []
        total_fees=0
        objs = Fees.objects.filter(madrasha=madrasha_instance.id, madrasha_class__id=student_class)
        for obj in objs:
            first_term_bool = obj.is_first_term
            second_term_bool = obj.is_second_term
            third_term_bool = obj.is_third_term
            term_activation_date = obj.examination_fee_active_from.strftime("%Y-%m-%d")
            term_date = datetime.strptime(term_activation_date, "%Y-%m-%d")
            term_fee = obj.amount
            if first_term_bool:
                if(current_date >= term_date):
#                 get_exam_fees = FessInfo.objects.filter(student=student_id, fees_type=fees_type,fees_type_term=ExamTerm.FIRST_TERM.value,
                #                                                                                                  paid_date__year=today.strftime("%Y"))
                   get_exam_fees = FessInfo.objects.filter(student=student_id, fees_type=fees_type,fees_type_term=ExamTerm.FIRST_TERM.value)
                   if not get_exam_fees:
                       data = {'term_name': ExamTerm.FIRST_TERM.value, 'amount': term_fee,'term_activation_date':term_activation_date}
                       term_fees.append(data)
                       total_fees +=term_fee
            if second_term_bool:
               if(current_date >= term_date):
                  get_exam_fees = FessInfo.objects.filter(student=student_id, fees_type=fees_type,fees_type_term=ExamTerm.SECOND_TERM.value)
                  if not get_exam_fees:
                      data = {'term_name': ExamTerm.SECOND_TERM.value, 'amount': term_fee,'term_activation_date':term_activation_date}
                      term_fees.append(data)
                      total_fees +=term_fee

            if third_term_bool:
                if(current_date >= term_date):
                   get_exam_fees = FessInfo.objects.filter(student=student_id, fees_type=fees_type,fees_type_term=ExamTerm.THIRD_TERM.value)
                   if not get_exam_fees:
                       data = {'term_name': ExamTerm.THIRD_TERM.value, 'due_amount': term_fee,'term_activation_date':term_activation_date}
                       term_fees.append(data)
                       total_fees +=term_fee
        return ({"status": 200, "fees_type": fees_type, 'total_amount':total_fees,"term_fees": term_fees})

    else:
        if (fees_type == FeesType.MONTHLY_TUITION.value):
            if is_tution_fee_active:
                date_1 = tution_fee_active_from
            else:
                return ({"status": 204, "fees_type": fees_type, "msg": "Tution Fee is not activated"})
        elif (fees_type == FeesType.BOARDING.value):
            if is_boarding_fee_active:
                date_1 = boarding_fee_active_from
            else:
                return ({"status": 204, "fees_type": fees_type, "msg": "Boarding Fee is not activated"})
        elif (fees_type == FeesType.TRANSPORT.value):
            if is_transport_fee_active:
                date_1 = transport_fee_active_from
            else:
                return ({"status": 204, "fees_type": fees_type, "msg": "Transport Fee is not activated"})
        else:
            date_1 = today.strftime("%Y-%m-%d")

        date_2 = today.strftime("%Y-%m-%d")
        start = datetime.strptime(date_1, "%Y-%m-%d")
        end = datetime.strptime(date_2, "%Y-%m-%d")
        res = (end.year - start.year) * 12 + (end.month - start.month)
        month_difference = res
        print(student_inactance.monthly_tution_fee)
        get_all_paid_fees = FessInfo.objects.values('paid_date','current_fee').annotate(name_count=Count('paid_date'),paid_amount=Sum('paid_amount')).filter(student=student_id, fees_type=fees_type).order_by('paid_date')
        print("fees list ", get_all_paid_fees)
        due_fees = []
        months = []
        for month in range(int(month_difference)):
            month += 1
            first = today.replace(day=31)
            last_month = first - timedelta(days=31 * month)
            months.append(last_month.strftime("%Y-%m"))
        total_due = 0
#         test = FessInfo.objects.values('paid_date','paid_amount').annotate(paid_date=Count('paid_date')).filter(paid_date_count__gt=1)
#         test1= FessInfo.objects.values('paid_date').annotate(Count('id')).order_by().filter(id__count__gt=1)
#         get_duplicate = FessInfo.objects.values('paid_date').annotate(name_count=Count('paid_date'),paid_amount=Sum('paid_amount'))
#         get_unique = FessInfo.objects.values('paid_date').annotate(name_count=Count('paid_date'),paid_amount=Sum('paid_amount')).exclude(name_count=1)
#         print("duplicate",get_unique)

        for fees in get_all_paid_fees:
            date = fees['paid_date'].strftime("%Y-%m")
            paid_amount = fees['paid_amount']
            current_fee = fees['current_fee']
            due_amount = current_fee - paid_amount
            due_amount = current_fee - paid_amount
            if (date in months):
#                 print("dus month ", date)
                months.remove(date)
            if (paid_amount < current_fee):
                #                 print("fees list ",fees.paid_date)
                #                 print("fees amount ",fees.paid_amount)
                #                 print("current amount ",fees.current_fee)
                total_due += due_amount
                data = {'date': str(date), 'due_amount': due_amount}
                due_fees.append(data)
        for due_date in months:
            total_due += int(monthly_tution_fee)
            data = {'id': '', 'date': str(due_date), 'due_amount': monthly_tution_fee}
            due_fees.append(data)
#         print(months)
        response = {
            "status": 200,
            "fees_type": fees_type,
            "total_amount": total_due,
            "data": due_fees
        }
        return response


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
        created_by = user.objects.get(id=requested_data['user_id'])
        student_inactance = Student.objects.get(id=requested_data['student'])

        madrasha = requested_data['madrasha']
        total_amount = requested_data['total_amount']
        paid_date = requested_data['paid_date']


        student_income = {
            "madrasha": madrasha,
            "student": student,
            "total_amount": total_amount,
            "paid_date": paid_date,
            "created_by": created_by
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
            from_date = obj["from_date"]
            if from_date:
                from_date = datetime.strptime(str(), date_format)
                to_date = datetime.strptime(str(from_date), date_format)
                date_difference = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
                month_value = date_difference + 1
                print(month_value)


            fees_type = obj['fees_type']
            paid_amount =  obj["paid_amount"]
            current_fee=obj["current_fee"]
            fees_type_term=obj["fees_type_term"]
            print("paid_amount1 ",paid_amount)
            get_unpaid_data = GetStudentIncomeUnpaid(student, madrasha, fees_type)

#             if ((fees_type == FeesType.MONTHLY_TUITION.value) or (fees_type ==FeesType.BOARDING.value) or (fees_type ==FeesType.TRANSPORT.value)):
            if fees_type in [FeesType.MONTHLY_TUITION.value, FeesType.BOARDING.value,FeesType.TRANSPORT.value]:
                print("this will do the calculation")
                if from_date is "":
    #               print("test View",get_unpaid_data)
                    for payment in get_unpaid_data["data"]:
                        payment_date = payment['date']
                        payment_due = int(payment['due_amount'])
                        if(paid_amount>=payment_due):
                            print("payment ",payment['date'])
                            print("Amount ",payment['due_amount'])
                            FessInfo.objects.create(
                                madrasha=madrasha_instance,
                                student=student_inactance,
                                student_income=student_income_id,
                                current_fee=current_fee,
                                fees_type=fees_type,
                                fees_type_term=fees_type_term,
                                paid_date=payment_date+'-01',
                                paid_amount=payment_due
                            )
                            paid_amount=paid_amount-payment_due
                        else:
                            FessInfo.objects.create(
                                madrasha=madrasha_instance,
                                student=student_inactance,
                                student_income=student_income_id,
                                current_fee=current_fee,
                                fees_type=fees_type,
                                fees_type_term=fees_type_term,
                                paid_date=payment_date+'-01',
                                paid_amount=paid_amount
                            )
                            break

                print("paid_amount2 ",paid_amount)
                return Response(get_unpaid_data)

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

            if (fees_type == FeesType.ADMISSION.value):
                FessInfo.objects.create(
                    madrasha=madrasha_instance,
                    student=student_inactance,
                    student_income=student_income_id,
                    current_fee=current_fee,
                    fees_type=fees_type,
                    fees_type_term=fees_type_term,
                    paid_date=paid_date,
                    paid_amount=paid_amount
                )
            if (fees_type == FeesType.EXAMINATION.value):
                if fees_type_term:
                    FessInfo.objects.create(
                        madrasha=madrasha_instance,
                        student=student_inactance,
                        student_income=student_income_id,
                        current_fee=current_fee,
                        fees_type=fees_type,
                        fees_type_term=fees_type_term,
                        paid_date=paid_date,
                        paid_amount=paid_amount
                    )

        return Response({"status": True, "message": "Operation has been done successfully"})


class StudentIncomeGetUnpaidView(APIView):
    def post(self, request, madrasha_slug, formate=None):
        print("method ", request)
        requested_data = request.data
        student = requested_data["student"]
        madrasha = requested_data['madrasha']
        fees_type = requested_data['fees_type']

        get_unpaid_data = GetStudentIncomeUnpaid(student, madrasha, fees_type)
        return Response(get_unpaid_data)


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
        student_fees =  FessInfo.objects.filter(student_income__id=student_income.id).values()
        serializer = StudentIncomeListSerializer(student_income)
        return Response({"status": True, "income_fees":student_fees, "data": serializer.data})

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
