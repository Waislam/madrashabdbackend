from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    VehicleInfo,
    TransportDetail,
)
from .serializers import (
    VehicleInfoListSerializers,
    VehicleInfoSerializers,
    TransportDetailListSerializers,
    TransportDetailSerializers
)

from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import (
    VehicleInfoFilter,
    TransportDetailFilter
)

from rest_framework.generics import mixins, GenericAPIView
from students.models import Student


# VehicleInfo 1. =======================================

class VehicleInfoListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    queryset = VehicleInfo.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = VehicleInfoSerializers
    filterset_class = VehicleInfoFilter
    search_fields = ['car_number', 'driver_name', 'driver_number']
    pagination_class = CustomPagination

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(VehicleInfoListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get(self, request, *args, **kwargs):
        """method to show the list of Committee """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Committee obj """
        # print('kwargs', **kwargs)
        return self.create(request, *args, **kwargs)


class VehicleInfoDetail(APIView):
    """
    Retrieve, update or delete a VehicleInfo instance.
    """

    def get_object(self, pk):
        try:
            return VehicleInfo.objects.get(pk=pk)
        except VehicleInfo.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = VehicleInfoListSerializers(queryset)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update single obj details"""
        queryset = self.get_object(pk)
        serializer = VehicleInfoSerializers(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True,
                 "message": "VehicleInfo has been updated successfully",
                 "data": serializer.data,
                 }
            )
        return Response(
            {"status": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# TransportListView 2. =======================================

class TransportListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    queryset = TransportDetail.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TransportDetailFilter
    search_fields = ['car_number', 'car_name']
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TransportDetailListSerializers
        return TransportDetailSerializers

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(TransportListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get(self, request, *args, **kwargs):
        """method to show the list of Committee """
        return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     """Method to create Committee obj """
    #     print("value")
    #     # print('kwargs', **kwargs)
    #     return self.create(request, *args, **kwargs)


class TransportPostrequestView(APIView):
    """creating Transport obj"""
    def post(self, request, student_id, *args, **kwargs):
        student = Student.objects.get(student_id=student_id)

        serializer = TransportDetailSerializers(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.validated_data['student_id'] = student
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransportDetailView(APIView):
    """
    Retrieve, update or delete a TransportDetail instance.
    """

    def get_object(self, pk):
        try:
            return TransportDetail.objects.get(pk=pk)
        except TransportDetail.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = TransportDetailListSerializers(queryset)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update single obj details"""
        queryset = self.get_object(pk)
        serializer = TransportDetailSerializers(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True,
                 "message": "TransportDetail has been updated successfully",
                 "data": serializer.data,
                 }
            )
        return Response(
            {"status": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
