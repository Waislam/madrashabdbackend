from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from .serializers import StudentSerializer, StudentListSerializer, StudentSerializerUpdate
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework import status
from .models import Student
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import StudentFilter
from dateutil import relativedelta


class StudentView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    """Student Create and list view"""

    queryset = Student.objects.all()
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = StudentFilter
    # search_fields = ["student_id"]
    # pagination_class = CustomPagination
    # permission_classes = [IsMadrashaAdmin]

    # def check_permissions(self):
    #     pass

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(StudentView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StudentListSerializer
        return StudentSerializer

    def get(self, request, *args, **kwargs):
        """method to show the list of Students"""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create student obj"""
        return self.create(request, *args, **kwargs)


class StudentDetailView(APIView):
    """this class is for CRUD"""
    def get_object(self, slug):
        """For getting single obj with slug field"""
        try:
            return Student.objects.get(slug=slug)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, slug, formate=None):
        """For getting single student details"""
        student = self.get_object(slug)
        serializer = StudentListSerializer(student)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, slug, formate=None):
        """update single obj details"""
        student = self.get_object(slug)
        serializer = StudentSerializerUpdate(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "student profile has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response(
            {"status": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class StudentDetailBySlugView(APIView):
    """this class is for CRUD"""
    def get_object(self, student_id):
        """For getting single obj with slug field"""
        try:
            return Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, student_id, formate=None):
        """For getting single student details"""
        try:
            student = self.get_object(student_id)
            serializer = StudentListSerializer(student)
            return Response({"status": True, "data": serializer.data})
        except:
            return Response({"status": False})


class CheckUniquePassportNumber(APIView):

    def get(self, request, passport_number, formate=None):
        """For getting single student details"""
        try:
            if passport_number:
                Student.objects.get(passport_number=passport_number)
                return Response({"status": True, "msg": "Passport number already exist!!"})
            else:
                return Response({"status": False, "msg": "Passport number is not present!!"})
        except:
            return Response({"status": False, "msg": "Passport number is not present!!"})


class CheckUniqueNIDNumber(APIView):

    def get(self, request, nid_number, formate=None):
        """For getting single student details"""
        try:
            if nid_number:
                Student.objects.get(student_nid=nid_number)
                return Response({"status": True, "msg": "NID number already exist!!"})
            else:
                return Response({"status": False, "msg": "NID number is not present!!"})
        except:
            return Response({"status": False, "msg": "NID number is not present!!"})
