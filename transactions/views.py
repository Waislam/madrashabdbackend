from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from datetime import datetime, timedelta
from enum import Enum
from accounts.models import Madrasha
from committees.models import PermanentMembers
from students.models import Student, FessInfo
from settingapp.models import Fees
from students.serializers import FessInfoSerializer
from .serializers import (IncomeCategorySerializer, IncomeSubCategorySerializer, StudentIncomeSerializer,
                          OtherIncomeSerializer,
                          OtherIncomeListSerializer, StudentIncomeListSerializer,OtherIncomeListSerializerV2, AllExpenseListSerializer,
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
import json
from django.conf import settings
from settingapp.views import SendSMS

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

class MemrberType(Enum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

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
                monthly_fees = student_inactance.monthly_tution_fee
            else:
                return ({"status": 204, "fees_type": fees_type, "msg": "Tution Fee is not activated"})
        elif (fees_type == FeesType.BOARDING.value):
            if is_boarding_fee_active:
                monthly_fees = student_inactance.boarding_feee
                date_1 = boarding_fee_active_from
            else:
                return ({"status": 204, "fees_type": fees_type, "msg": "Boarding Fee is not activated"})
        elif (fees_type == FeesType.TRANSPORT.value):
            if is_transport_fee_active:
                monthly_fees = student_inactance.transport_fee
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
#         print(student_inactance.monthly_fees)
        get_all_paid_fees = FessInfo.objects.values('paid_date','current_fee').annotate(name_count=Count('paid_date'),paid_amount=Sum('paid_amount')).filter(student=student_id, fees_type=fees_type)
#         print("fees list ", get_all_paid_fees)
#         print("month_difference ", month_difference)
        due_fees = []
        months = []
        for month in range(int(month_difference)):
            month += 1
            first = today.replace(day=31)
            last_month = first - timedelta(days=31 * month)
            months.append(last_month.strftime("%Y-%m"))
#         print("months1 ", months)
#         test = FessInfo.objects.values('paid_date','paid_amount').annotate(paid_date=Count('paid_date')).filter(paid_date_count__gt=1)
#         test1= FessInfo.objects.values('paid_date').annotate(Count('id')).order_by().filter(id__count__gt=1)
#         get_duplicate = FessInfo.objects.values('paid_date').annotate(name_count=Count('paid_date'),paid_amount=Sum('paid_amount'))
#         get_unique = FessInfo.objects.values('paid_date').annotate(name_count=Count('paid_date'),paid_amount=Sum('paid_amount')).exclude(name_count=1)
#         print("duplicate",get_unique)
        total_due = 0
        for fees in get_all_paid_fees:
            date = fees['paid_date'].strftime("%Y-%m")
#             print("Date ", date)
            paid_amount = fees['paid_amount']
            monthly_fee = fees['current_fee']
            print("monthly_fee == ", monthly_fee)
            due_amount = monthly_fee - paid_amount
            if (date in months):
#                 print("dus month ", date)
                months.remove(date)
            if (paid_amount < monthly_fee):
                #                 print("fees list ",fees.paid_date)
                #                 print("fees amount ",fees.paid_amount)
                #                 print("current amount ",fees.current_fee)
                total_due += due_amount
                data = {'date': str(date), 'due_amount': due_amount, 'monthly_fee': monthly_fee}
                due_fees.append(data)
        print("months2 ", months)
        for due_date in months:
            total_due += int(monthly_fees)
            data = {'date': str(due_date), 'due_amount': monthly_fees,'monthly_fee': monthly_fees}
            due_fees.append(data)
#         print(months)
        get_upfront_fees = FessInfo.objects.filter(student=student_id, fees_type=fees_type,paid_date__gte=today.strftime("%Y-%m-%d"))
        upfront=[]
        for obj in get_upfront_fees:
            data = {'paid_date': obj.paid_date.strftime("%Y-%m-%d"), 'paid_amount': obj.paid_amount, 'fees_type': obj.fees_type,'fees_type_term':obj.fees_type_term}
            upfront.append(data)
        print(upfront)
        response = {
            "status": 200,
            "fees_type": fees_type,
            "total_amount": total_due,
            "data": due_fees,
            "upfront":upfront
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
        student_id = Student.objects.get(id=student)

        madrasha_instance = Madrasha.objects.get(id=requested_data['madrasha'])
        created_by = user.objects.get(id=requested_data['user_id'])
        student_inactance = Student.objects.get(id=requested_data['student'])

        student_phone = student_inactance.user.phone

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
        last_receipt_number = StudentIncome.objects.last().receipt_number
        fees = []
        for obj in requested_data['fees_detail']:
            date_format = "%Y-%m-%d"
            from_date = obj["from_date"]
            to_date = obj["to_date"]
            if from_date:
                date_1 = str(from_date)
                date_2 = str(to_date)
                start = datetime.strptime(date_1, "%Y-%m-%d")
                end = datetime.strptime(date_2, "%Y-%m-%d")
                difference=(end.year - start.year) * 12 + (end.month - start.month)
                month_value = difference + 1
                print(month_value)

            fees_type = obj['fees_type']
            paid_amount =  obj["paid_amount"]
            paid_amount_v2 =  obj["paid_amount"]
            current_fee=obj["current_fee"]
            fees_type_term=obj["fees_type_term"]
            print("paid_amount1 ",paid_amount)
            get_unpaid_data = GetStudentIncomeUnpaid(student, madrasha, fees_type)
            total_due_amount = get_unpaid_data["total_amount"]
#             print("get_unpaid_data",get_unpaid_data)
#             if ((fees_type == FeesType.MONTHLY_TUITION.value) or (fees_type ==FeesType.BOARDING.value) or (fees_type ==FeesType.TRANSPORT.value)):
            monthly_paid_count = 0
            admission_paid_count = 0
            exam_paid_count = 0
            if fees_type in [FeesType.MONTHLY_TUITION.value, FeesType.BOARDING.value, FeesType.TRANSPORT.value]:
#                 if(paid_amount>total_due_amount):
#                     temp_due_amount = paid_amount - total_due_amount
#                     print("temp_due_amount", temp_due_amount)

                if (total_due_amount > 0 ):
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
                                current_fee=payment['monthly_fee'],
                                fees_type=fees_type,
                                fees_type_term=fees_type_term,
                                paid_date=payment_date+'-01',
                                paid_amount=payment_due
                            )
                            paid_amount=paid_amount-payment_due
                            total_due_amount = total_due_amount - payment_due

                        else:
                            FessInfo.objects.create(
                                madrasha=madrasha_instance,
                                student=student_inactance,
                                student_income=student_income_id,
                                current_fee=payment['monthly_fee'],
                                fees_type=fees_type,
                                fees_type_term=fees_type_term,
                                paid_date=payment_date+'-01',
                                paid_amount=paid_amount
                            )
                            total_due_amount = total_due_amount - payment_due
                            paid_amount=0
                            break
                    monthly_paid_count +=1
                print("paid_amount2 ",paid_amount)
                if (total_due_amount == 0 and from_date !=""):
                    print("paid_amount33 === ",paid_amount)
                    print("total_due_amount 33 ",total_due_amount)
                    if month_value == 1:
                        obj["paid_date"] = from_date
                        FessInfo.objects.create(
                            madrasha=madrasha_instance,
                            student=student_inactance,
                            student_income=student_income_id,
                            current_fee=current_fee,
                            fees_type=fees_type,
                            paid_date=from_date,
                            paid_amount=current_fee
                        )
                        paid_amount=paid_amount-current_fee
                    else:
                        date_format = "%Y-%m-%d"
                        from_date = datetime.strptime(str(from_date), date_format)
                        x = from_date
                        full_year = x.year
                        month = x.month
                        days = x.day

                        for each in range(month_value):
                            from_date = str(full_year) + "-" + str(month + each) + "-" + str(days)
                            print("entry date", from_date)
                            FessInfo.objects.create(
                                madrasha=madrasha_instance,
                                student=student_inactance,
                                student_income=student_income_id,
                                current_fee=current_fee,
                                fees_type=fees_type,
                                # fees_type_term=obj["fees_type_term"]
                                paid_date=from_date,
                                paid_amount=current_fee
                            )
                            paid_amount=paid_amount-current_fee
                    monthly_paid_count +=1
#                 print("paid_amount3 ",paid_amount)
#                 print("total_due_amount ",total_due_amount)
#                 return Response(get_unpaid_data)



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
                admission_paid_count +=1
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
                    exam_paid_count +=1

            if monthly_paid_count>0 or admission_paid_count> 0 or exam_paid_count>0:
                msg = "You have successfully paid "+str(total_amount)+" TK. Money receipt number is " + str(last_receipt_number)
                if student_phone:
                    SendSMS(student_phone,msg)

        return Response({"status": True, "message": "Operation has been done successfully"})


class StudentIncomeGetUnpaidView(APIView):
    def post(self, request, madrasha_slug, formate=None):
        print("method ", request)
        today = datetime.now()
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
    # pagination_class = CustomPagination

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
        requested_data = request.data
        madrasha_instance = Madrasha.objects.get(id=requested_data['madrasha'])
        created_by = user.objects.get(id=requested_data['user_id'])

        obj_length = len(requested_data['other_details'])
        count = 0
        for obj in requested_data['other_details']:
            if obj['member_type'] not in [MemrberType.MONTHLY.value,MemrberType.YEARLY.value]:
                category_instance = IncomeCategory.objects.get(id=obj['category'])
                sub_category_instance = IncomeSubCategory.objects.get(id=obj['sub_category'])
                member_instance=None
            else:
                member_instance = PermanentMembers.objects.get(id=obj['member'])
                category_instance=None
                sub_category_instance=None


            donar_name=obj['donar_name']
            member_type=obj['member_type']
            paid_date=obj['paid_date']
            amount=obj['amount']
            address=obj['address']
            receipt_book_number=obj['receipt_book_number']
            receipt_page_number=obj['receipt_page_number']
            if count == 0:
                OtherIncome.objects.create(
                    madrasha=madrasha_instance,
                    category=category_instance,
                    sub_category=sub_category_instance,
                    donar_name=donar_name,
                    member=member_instance,
                    member_type=member_type,
                    amount=amount,
                    address=address,
                    paid_date=paid_date,
                    receipt_book_number=receipt_book_number,
                    receipt_page_number=receipt_page_number,
                    created_by = created_by
                )
            else:
                last_receipt_number = OtherIncome.objects.last().receipt_number
                OtherIncome.objects.create(
                madrasha=madrasha_instance,
                category=category_instance,
                sub_category=sub_category_instance,
                donar_name=donar_name,
                member=member_instance,
                member_type=member_type,
                amount=amount,
                address=address,
                paid_date=paid_date,
                receipt_book_number=receipt_book_number,
                receipt_page_number=receipt_page_number,
                receipt_number = last_receipt_number,
                created_by = created_by
            )
            count+=1
        return Response(
            {
                "status": True,
                "message": "Other Income has been Insert successfully",
            }
        )


class OtherIncomeDetailView(APIView):
    """this class is for CRUD"""

    def get_object(self, receipt_number):
        """For getting single obj with slug field"""
        try:
            other_income_details = OtherIncome.objects.filter(receipt_number=receipt_number)
            return other_income_details
        except OtherIncome.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """For getting single object details"""
        other_income = self.get_object(pk)
        serializer = OtherIncomeListSerializerV2(other_income, many=True).data
        return Response({"status": True, "data": serializer})

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

class OtherIncomeGetUnpaidView(APIView):
    def post(self, request, formate=None):
        print("method ", request)
        requested_data = request.data
        member_id = requested_data['member_id']
        madrasha_id = requested_data['madrasha']
        member_type = requested_data['member_type']
        today = datetime.now()
        try:
            member_instance = PermanentMembers.objects.get(id=member_id)
            if member_instance:
                if (member_type == MemrberType.MONTHLY.value):
                    if member_instance.is_monthly_contribution and member_instance.monthly_activation_date:
                        member_activation_date = member_instance.monthly_activation_date
                        member_contribution_amount = member_instance.monthly_contribution
                        is_member_active = member_instance.is_monthly_contribution

                    else:
                        return Response({"status": False, "member_id":member_id,'msg':"Member is not activated properly"})
                        is_member_active = False

                if (member_type == MemrberType.YEARLY.value):
                    if member_instance.is_yearly_contribution and member_instance.yearly_activation_date:
                        member_activation_date = member_instance.yearly_activation_date
                        member_contribution_amount = member_instance.yearly_contribution
                        is_member_active = member_instance.is_yearly_contribution

                    else:
                        return Response({"status": False, "member_id":member_id,'member_type':member_type,'msg':"Member is not activated properly"})

            date_1 = member_activation_date.strftime("%Y-%m-%d")
            date_2 = today.strftime("%Y-%m-%d")
            start = datetime.strptime(date_1, "%Y-%m-%d")
            end = datetime.strptime(date_2, "%Y-%m-%d")
            if (member_type == MemrberType.MONTHLY.value):
                difference=(end.year - start.year) * 12 + (end.month - start.month)
            if (member_type == MemrberType.YEARLY.value):
                difference = (end.year - start.year)
            amount_to_pay = difference*member_contribution_amount
            get_all_paid = OtherIncome.objects.values('member').annotate(name_count=Count('member'),amount=Sum('amount')).filter(madrasha=madrasha_id,member=member_id, member_type=member_type)

            if get_all_paid:
                total_paid_amount = get_all_paid[0]['amount']
            else:
                total_paid_amount = 0
            if(amount_to_pay>=total_paid_amount):
                total_due_amount = amount_to_pay-total_paid_amount
                total_upfront_amount = 0
            else:
                total_due_amount = 0
                total_upfront_amount = total_paid_amount-amount_to_pay

            return Response({"status": True, "member_id":member_id,'amount_to_pay':amount_to_pay,'total_paid_amount':total_paid_amount,'total_due_amount':total_due_amount,'total_upfront_amount':total_upfront_amount,'member_activation_date':member_activation_date})

        except PermanentMembers.DoesNotExist:
            return Response({"status": False, "msg":"member id not found"},status=status.HTTP_400_BAD_REQUEST,)

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
