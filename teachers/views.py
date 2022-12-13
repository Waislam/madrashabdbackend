from django.shortcuts import render
from django.http import Http404
from .serializers import TeacherSerializer, TeacherListSerializer, TeacherUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Teacher
from students.pagination import CustomPagination
from .filters import TeacherFilter
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import mixins, GenericAPIView


class TeacherView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericAPIView
):
    """ teacher Create and list view """
    queryset = Teacher.objects.all()
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = TeacherFilter
    # search_fields = ['teacher_id']
    # pagination_class = CustomPagination

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super(TeacherView, self).get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TeacherListSerializer
        return TeacherSerializer

    def get(self, request, *args, **kwargs):
        """method to show the list of Teacher """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Teacher obj """
        return self.create(request, *args, **kwargs)


class TeacherDetailView(APIView):
    """ put, get, no delete"""

    def get_object(self, slug):
        """get single obj"""
        try:
            return Teacher.objects.get(slug=slug)
        except Teacher.DoesNotExist:
            raise Http404

    def get(self, request, slug, formate=None):
        """veiw details of single obj"""
        teacher = self.get_object(slug)
        serializer = TeacherListSerializer(teacher)
        return Response({'status': True, 'data': serializer.data})

    def put(self, request, slug, formate=None):
        """update single teacher"""
        teacher = self.get_object(slug)
        serializer = TeacherUpdateSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'data': serializer.data})
        return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
