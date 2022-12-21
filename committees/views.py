from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Committee,
    PermanentMembers,
    OtherMembers
)
from .serializers import (
    CommitteeSerializers,
    CommitteeListSerializers,
    PermanentMembersListSerializers,
    PermanentMembersSerializers,
    OthersMemberListSerializers,
    OthersMemberSerializers
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import (
    CommitteeFilter,
    PermanentMembersFilter,
    OtherMembersFilter
)
from .pagination import CustomPagination
from rest_framework.generics import mixins, GenericAPIView


# Committee 1. =======================================

class CommitteeListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    queryset = Committee.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = CommitteeSerializers
    filterset_class = CommitteeFilter
    search_fields = ['member_name', 'phone_number']
    pagination_class = CustomPagination

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(CommitteeListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get(self, request, *args, **kwargs):
        """method to show the list of Committee """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Committee obj """
        # print('kwargs', **kwargs)
        return self.create(request, *args, **kwargs)


class CommitteeDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Committee.objects.get(pk=pk)
        except Committee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = CommitteeListSerializers(queryset)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update single obj details"""
        queryset = self.get_object(pk)
        serializer = CommitteeSerializers(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True,
                 "message": "Student Income has been updated successfully",
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


# PermanentMembersListView 2. ======================

class PermanentMembersListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    queryset = PermanentMembers.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = PermanentMembersSerializers
    filterset_class = PermanentMembersFilter
    search_fields = ['member_name', 'phone_number']
    pagination_class = CustomPagination

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(PermanentMembersListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get(self, request, *args, **kwargs):
        """method to show the list of Committee """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Committee obj """
        # print('kwargs', **kwargs)

        return self.create(request, *args, **kwargs)


class PermanentMembersDetail(APIView):
    """
    Retrieve, update or delete a PermanentMembers instance.
    """

    def get_object(self, pk):
        try:
            return PermanentMembers.objects.get(pk=pk)
        except PermanentMembers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = PermanentMembersListSerializers(queryset)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update single obj details"""
        queryset = self.get_object(pk)
        serializer = PermanentMembersSerializers(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True,
                 "message": "PermanentMembers has been updated successfully",
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
        context = {
            "status": True,
            "message": "PermanentMembers has been delete successfully",
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)


# OtherMembers 3. ======================

class OtherMembersListView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    queryset = OtherMembers.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = OthersMemberSerializers
    filterset_class = OtherMembersFilter
    search_fields = ['member_name', 'phone_number']
    pagination_class = CustomPagination

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(OtherMembersListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get(self, request, *args, **kwargs):
        """method to show the list of Committee """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Committee obj """
        # print('kwargs', **kwargs)
        return self.create(request, *args, **kwargs)


class OtherMembersDetail(APIView):
    """
    Retrieve, update or delete a OtherMembers instance.
    """

    def get_object(self, pk):
        try:
            return OtherMembers.objects.get(pk=pk)
        except OtherMembers.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = OthersMemberListSerializers(queryset)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update single obj details"""
        queryset = self.get_object(pk)
        serializer = OthersMemberSerializers(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": True,
                 "message": "OtherMembers has been updated successfully",
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
        context = {
            "status": True,
            "message": "OtherMembers has been delete successfully",
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)
