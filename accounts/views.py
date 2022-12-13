'''
1.dependent drop down for address
2. individual address
3. MadrashaView
4. UserRegistration
5. TokenAuthentication
6. MadrashaUserListing
7. AvatarUpdateView
'''
import json

from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from .models import *
from .serializers import (
    AddressSerializer,
    MadrashaSerializer,
    RegistrationSerializer,
    MadrashaUserListingSerializer,
    AvatarUpdateSerializer,
    CustomUserSerializer,
    DistrictSerializer,
    DivisionSerializer,
    ThanaSerializer,
    PostOfficeSerializer,
    PostCodeSerializer,
    CustomUserLoginSerializer,
    MadrashaLoginSerializer
)

from rest_framework import status, generics
from rest_framework.generics import mixins, GenericAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from .filters import DistrictFilter, PostCodeFilter, PostOfficeFilter, ThanaFilter

User = get_user_model()


# Create your views here.

#  ====================================== 1.dependent drop down for address ==========================

class DivisionListView(ListAPIView):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer


class DistrictListView(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        queryset = District.objects.all()
        division = self.kwargs.get('division')
        if division is not None:
            queryset = queryset.filter(division__pk=division)
        return queryset


class ThanaListView(ListAPIView):
    queryset = Thana.objects.all()
    serializer_class = ThanaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ThanaFilter


class ThanaListViewWithDependency(generics.ListAPIView):
    serializer_class = ThanaSerializer

    def get_queryset(self):
        queryset = Thana.objects.all()
        district = self.kwargs.get('district')
        if district is not None:
            queryset = queryset.filter(district__pk=district)
        return queryset


class PostOfficeListViewWithDependency(generics.ListAPIView):
    serializer_class = PostOfficeSerializer

    def get_queryset(self):
        queryset = PostOffice.objects.all()
        district = self.kwargs.get('district')
        if district is not None:
            queryset = queryset.filter(district__pk=district)
        return queryset

# class PostOfficeList(APIView):
#     def post(self, request):
#         district = request.data['district']
#         post_office = {}
#         if district:
#             post_offices = District.objects.get(id=district).postoffices.all()
#             post_office = {d.name: d.id for d in post_offices}
#         return JsonResponse(data=post_office, safe=False)


class PostOfficeListView(ListAPIView):
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostOfficeFilter


# class PostCodeList(APIView):
#     def post(self, request):
#         post_office = request.data['post_office']  # here post_code is the var from form
#         post_code = {}
#         if post_office:
#             post_codes = PostCode.objects.get(id=post_office).postcodess.all()
#             post_code = {d.name: d.id for d in post_codes}
#         return JsonResponse(data=post_code, safe=False)


class PostCodeListView(ListAPIView):
    queryset = PostCode.objects.all()
    serializer_class = PostCodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostCodeFilter


class PostCodeListViewWithDependency(generics.ListAPIView):
    serializer_class = PostCodeSerializer

    def get_queryset(self):
        queryset = PostCode.objects.all()
        post_office = self.kwargs.get('post_office')
        if post_office is not None:
            queryset = queryset.filter(post_office__pk=post_office)
        return queryset

# ==================== 2. individual address ============


class AddressDetail(APIView):
    def get_object(self, pk):
        try:
            return Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)


# ===================== 3. MadrashaView ============

class MadrashaView(APIView):

    def get(self, request, formate=None):
        """
        Madrasha List api
        """
        madrshas = Madrasha.objects.all()
        serializer = MadrashaSerializer(madrshas, many=True)
        return Response({'status': True, 'data': serializer.data})

    def post(self, request, formate=None):
        """
        Create Madrasha api
        """
        serializer = MadrashaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'Madrasha has been created', 'data': serializer.data})
        return Response({'status': False, 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MadrashaDetailView(APIView):

    def get_object(self, slug):
        """ get single madrasha obj"""
        try:
            return Madrasha.objects.get(slug=slug)
        except Madrasha.DoesNotExist:
            return Http404

    def get(self, request, slug, formate=None):
        """ Single Madrasha detail view api"""
        madrasha = self.get_object(slug)
        serializer = MadrashaSerializer(madrasha)
        return Response({'status': True, 'data': serializer.data})

    def put(self, request, slug, formate=None):
        """ update madrasha api"""
        madrasha = self.get_object(slug)
        serializer = MadrashaSerializer(madrasha, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'Madrasha has been updated'})


# ======================== 4. UserRegistration ================

class UserRegistrationView(APIView):
    """Create and get user"""

    def post(self, request, formate=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(phone=serializer.data.get('phone'))
            return Response({'status': True, 'data': serializer.data, 'user_id': user.id})
        return Response({'status': False, 'message': serializer.errors})


# ==================== 5. TokenAuthentication ===================
class CustomAuthToken(ObtainAuthToken, APIView):

    def get(self, request, formate=None):
        """get the user id using token"""
        token = request.COOKIES.get('token')
        user_id = Token.objects.get(key=token).customuser_id
        user = User.objects.get(id=user_id)
        if user.exists():
            return Response({'user': user})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = CustomUser.objects.get(pk=user.pk)

        user_madrasha = MadrashaUserListing.objects.get(user=user_data)
        madrasha = Madrasha.objects.get(slug=user_madrasha.madrasha.slug)
        user_info = CustomUserLoginSerializer(model_to_dict(user_data))

        return Response({
            'status': True,
            "data": user_info.data,
            "token": token.key,
            "role": "Admin",
            # 'user_madrasha_id': madrasha.pk,
            'user_madrasha_id': madrasha.pk,
            'user_madrasha_slug': madrasha.slug,
            'user_madrasha_code': madrasha.madrasha_code,
        })

        # if user_info.is_valid():
        #     print("user_info.data", user_info)
        #     return Response({'status': True, "data": user_info.data})
        # print("user_info.data", user_info.errors)
        # return Response({'status': False})
        # return Response({
        #     "user_data": user_info.data,
        #     'token': token.key,
        #     'user': user_mobile,
        #     'user_id': user.pk,
        #     'phone': user.phone,
        #     'user_madrasha_id': user_madrasha.pk,
        #     'user_madrasha_slug': user_madrasha.madrasha.slug,
        #     'user_madrasha_code': user_madrasha.madrasha.madrasha_code,
        # })


# =========================== 6. MadrashaUserListing =============================
class MadrashaUserListingView(mixins.ListModelMixin,
                              GenericAPIView):
    """api view for Madrashauser listing"""
    queryset = MadrashaUserListing.objects.all()
    serializer_class = MadrashaUserListingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user', 'madrasha']
    search_fields = ['user']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# ================== 7. AvatarUpdateView ===========
class AvatarUpdateView(APIView):
    """avatar update api for user"""

    def get_object(self, pk):
        """get the user object"""
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def put(self, request, pk, formate=None):
        user = self.get_object(pk)
        serializer = AvatarUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'message': 'img updated successfully'})
        return Response({'status': False, 'message': serializer.data})


class UserDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
