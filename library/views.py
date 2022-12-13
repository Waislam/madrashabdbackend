from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import mixins, GenericAPIView
from rest_framework.views import APIView

from library.filters import BookFilter, BookDistributionFilter
from library.models import LibraryBook, BookDistribution
from students.models import Student
from library.serializers import (
    LibraryBookCreateSerializer,
    LibraryBookUpdateSerializer,
    BookDistributionSerializer,
    BookDistributionPostSerializer
)
from students.pagination import CustomPagination


class LibaryBookView(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericAPIView):
    queryset = LibraryBook.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = LibraryBookCreateSerializer
    filterset_class = BookFilter
    search_fields = ['number']
    pagination_class = CustomPagination

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(LibaryBookView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get(self, request, *args, **kwargs):
        """method to show the list of Teacher """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Teacher obj """
        # print('kwargs', **kwargs)
        return self.create(request, *args, **kwargs)


class BookDetailView(APIView):
    """ put, get, no delete"""

    def get_object(self, pk):
        """get single obj"""
        try:
            return LibraryBook.objects.get(id=pk)
        except LibraryBook.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """veiw details of single obj"""
        book = self.get_object(pk)
        serializer = LibraryBookCreateSerializer(book)
        return Response({'status': True, 'data': serializer.data})

    def put(self, request, pk, formate=None):
        """update single teacher"""
        book = self.get_object(pk)
        serializer = LibraryBookUpdateSerializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'data': serializer.data})
        return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookDistributionListView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               GenericAPIView):
    queryset = BookDistribution.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = BookDistributionSerializer
    filterset_class = BookDistributionFilter
    search_fields = ('book_number__name', 'recipient_number')

    pagination_class = CustomPagination

    def get_queryset(self):
        """getting any argument/parameter from api/url"""
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(BookDistributionListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get(self, request, *args, **kwargs):
        """method to show the list of Teacher """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Method to create Teacher obj """
        # print('kwargs', **kwargs)
        return self.create(request, *args, **kwargs)


class BookDistributionDelete(APIView):
    """
    Retrieve, update or delete a BookDistribution instance.
    """
    
    def get_object(self, pk):
        try:
            return BookDistribution.objects.get(pk=pk)
        except BookDistribution.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        # queryset.book_number.is_available = True
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookDistributionPostAPI(APIView):

    def post(self, request, student_roll_id, book_number, *args, **kwargs):
        student = Student.objects.get(student_id=student_roll_id)
        book = LibraryBook.objects.get(id=book_number)

        serializer = BookDistributionPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['student_roll_id'] = student
            print("book... status: ", book.is_available)
            book.is_available = False
            book.save()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
