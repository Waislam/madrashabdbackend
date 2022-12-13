from django.http import Http404
from rest_framework import status, generics
from rest_framework.generics import mixins, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
# from .models import BazarList
# from .serializers import BazarListSerializer
# from .filters import BazarListFilter
from .pagination import CustomPagination
from rest_framework.views import APIView

from rest_framework.response import Response

from students.models import Student

from .models import KhabarDistribution, DailyBazar
from .serializers import DailyBazarListSerializer, DailyBazarSerializer


# class BazarListView(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     GenericAPIView
# ):
#     queryset = BazarList.objects.all()
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     serializer_class = BazarListSerializer
#     filterset_class = BazarListFilter
#     search_fields = ['date']
#     pagination_class = CustomPagination
#
#     def get_queryset(self):
#         """getting any argument/parameter from api/url"""
#         madrasha_slug = self.kwargs['madrasha_slug']
#         return super(BazarListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)
#         # return super(BazarListView, self).get_queryset()
#
#     def get(self, request, *args, **kwargs):
#         """method to show the list of Teacher """
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         """Method to create Teacher obj """
#         # print('kwargs', **kwargs)
#         return self.create(request, *args, **kwargs)

class DailyBazarView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = DailyBazar.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super(DailyBazarView, self).get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DailyBazarListSerializer
        return DailyBazarSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DailyBazarDetailView(APIView):

    def get_object(self, pk):
        try:
            return DailyBazar.objects.get(id=pk)
        except DailyBazar.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = DailyBazarListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = DailyBazarSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Daily Bazar has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class KhabarDistributionView(APIView):

    def post(self, request, madrasha_slug, student_id, date, meal_id):

        try:
            student = Student.objects.get(student_id=student_id)
            date = "1996-03-13"
            khabar = KhabarDistribution.objects.create(
                madrasha_id=1,
                student=student,
                date=date,
                is_breakfast=True
            )
            return Response({"status": True}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"status": False}, status=status.HTTP_400_BAD_REQUEST)



