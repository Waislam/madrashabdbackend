from django.shortcuts import render
from rest_framework import mixins, generics

from darul_ekama.models import SeatBooking, NigraniTable
from darul_ekama.serializers import (
    SeatBookingSerializer,
    SeatBookingListSerializer,
    NigraniTableListSerializer,
    NigraniTableSerializer
)
from settingapp.models import Seat
from students.models import Student
from teachers.models import Teacher
from rest_framework.views import APIView
from rest_framework import status


# Create your views here.
class SeatBookingView(mixins.CreateModelMixin,
                      mixins.ListModelMixin, generics.GenericAPIView
                      ):
    queryset = SeatBooking.objects.all()

    # serializer_class = SeatBookingSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SeatBookingListSerializer
        return SeatBookingSerializer

    def get_queryset(self):
        madrsha_slug = self.kwargs['madrasha_slug']
        queryset = super(SeatBookingView, self).get_queryset().filter(madrasha__slug=madrsha_slug)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        student_id = request.data['students']
        student = Student.objects.get(student_id=student_id)

        seat = Seat.objects.get(pk=request.data['seat'])
        seat.student = student
        seat.save()
        request.data['students'] = student.id
        return self.create(request, *args, **kwargs)

from django.http import Http404
from rest_framework.response import Response


class SeatBooingDetail(APIView):

    def get_object(self, pk):
        try:
            return SeatBooking.objects.get(pk=pk)
        except SeatBooking.DoesNotExist:
            raise Http404

    def delete(self, request, pk, formate=None):
        seat_booking = self.get_object(pk)
        seat_booking.seat.student = None
        seat_booking.seat.is_available = True
        seat_booking.seat.save()
        seat_booking.delete()
        return Response({"status": True, "msg": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class NigraniTableView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = NigraniTable.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs["madrasha_slug"]
        queryset = super(NigraniTableView, self).get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return NigraniTableListSerializer
        return NigraniTableSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        teacher_id = request.data['teacher']
        teacher = Teacher.objects.get(teacher_id=teacher_id).id
        request.data['teacher'] = teacher
        return self.create(request, *args, **kwargs)
