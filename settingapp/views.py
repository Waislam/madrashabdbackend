"""
1. Department
2. Designation
3. MadrashaClasses
4. MadrashaClassesGroup
5. Shift
6. Books
7. FeesCategory
8. Fees
9. Session
10. Exam rules
11. Buidling
"""
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from .models import Department, Designation, MadrashaClasses, MadrashaGroup, Shift, Session, Books, ExamRules, Fees, \
    Building, Room, Seat, FeesCategory
from .serializers import (DepartmentSerializer, DesignationSerializer, ClassSerializer, ClassGroupSerializer,
                          ShiftSerializer,
                          BooksSerializer, SessionSerializer, ExamRulesSerializer,
                          FeesSerializer, BuildingSerializer, SeatSerializer, SeatListSerializer,
                          FeesCategorySerializer, FeesCategoryListSerializer)

from .serializers import (DepartmentListSerializer,
                          DesignationListSerializer,
                          ClassListSerializer,
                          BooksListSerializer,
                          SessionListSerializer,
                          ClassGroupListSerializer,
                          ShiftListSerializer,
                          FeesListSerializer,
                          BuildingListSerializer,
                          RoomListSerializer,
                          RoomsSerializer
                          )

from django.conf import settings
import requests
import json
# Create your views here.

# ========================== 1. Department ===================================


class DepartmentView(APIView):
    """ A class to creae api for Department """

    def post(self, request, formate=None, **kwargs):
        """creating department object"""
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, **kwargs):
        """ showing a list of depatment objects"""
        department = Department.objects.filter(madrasha__slug=madrasha_slug)
        serializer = DepartmentListSerializer(department, many=True)
        return Response(serializer.data)


class DepartmentDetailview(APIView):
    """ department detail, update and delete"""

    def get_object(self, pk):
        """get single department obj"""
        try:
            return Department.objects.get(id=pk)
        except Department.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        department = self.get_object(pk)
        serializer = DepartmentListSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """delete"""
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ========================== 2. Designation ===================================


class DesignationView(APIView):
    """ A class to create api for Designation """

    def post(self, request, formate=None, **kwargs):
        """creating Designation object"""
        serializer = DesignationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None):
        """ showing a list of Designation objects"""
        designations = Designation.objects.filter(madrasha__slug=madrasha_slug)
        serializer = DesignationListSerializer(designations, many=True)
        return Response(serializer.data)


class DesignationDetailview(APIView):
    """ Designation detail, update and delete"""

    def get_object(self, pk):
        """get single Designation obj"""
        try:
            return Designation.objects.get(id=pk)
        except Designation.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details view for single obj"""
        designation = self.get_object(pk)
        serializer = DesignationListSerializer(designation)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        designation = self.get_object(pk)
        serializer = DesignationSerializer(designation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """delete"""
        designation = self.get_object(pk)
        designation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ========================== 3.MadrashaClasses ===================================


class MadrashaClassesView(APIView):
    """ A class to create api for MadrashaClasses """

    def post(self, request, formate=None, **kwargs):
        """creating MadrashaClasses object"""
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None):
        """ showing a list of MadrashaClasses objects"""
        classes = MadrashaClasses.objects.filter(madrasha__slug=madrasha_slug)
        serializer = ClassListSerializer(classes, many=True)
        return Response(serializer.data)


class MadrashaClassesDetailview(APIView):
    """ MadrashaClasses detail, update and delete"""

    def get_object(self, pk):
        """get single MadrashaClasses obj"""
        try:
            return MadrashaClasses.objects.get(id=pk)
        except MadrashaClasses.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        madrashaclass = self.get_object(pk)
        serializer = ClassListSerializer(madrashaclass)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        madrashaclass = self.get_object(pk)
        serializer = ClassSerializer(madrashaclass, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """delete"""
        madrashaclass = self.get_object(pk)
        madrashaclass.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ================================ 4. MadrashaClassesGroup =======================================

class MadrashaClassGroupView(APIView):
    """ A class to create api for MadrashaClassesGroup """

    def post(self, request, formate=None, **kwargs):
        """creating department object"""
        serializer = ClassGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None):
        """ showing a list of MadrashaClassesGroup objects"""
        groups = MadrashaGroup.objects.filter(madrasha__slug=madrasha_slug)
        serializer = ClassGroupListSerializer(groups, many=True)
        return Response(serializer.data)


class MadrashaClassGroupDetailview(APIView):
    """ MadrashaClassesGroup detail, update and delete"""

    def get_object(self, pk):
        """get single MadrashaClassesGroup obj"""
        try:
            return MadrashaGroup.objects.get(id=pk)
        except MadrashaGroup.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        madrashagroup = self.get_object(pk)
        serializer = ClassGroupListSerializer(madrashagroup)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        madrashagroup = self.get_object(pk)
        serializer = ClassGroupSerializer(madrashagroup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """delete"""
        madrashagroup = self.get_object(pk)
        madrashagroup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ================================== 5. Shift =====================

class ShiftView(APIView):
    """ A class to create api for Shift """

    def post(self, request, formate=None, **kwargs):
        """creating Shift object"""
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None):
        """ showing a list of Shift objects"""
        shifts = Shift.objects.filter(madrasha__slug=madrasha_slug, is_active=True)
        serializer = ShiftListSerializer(shifts, many=True)
        return Response(serializer.data)


class ShiftDetailview(APIView):
    """ Shift detail, update and delete"""

    def get_object(self, pk):
        """get single Shift obj"""

        try:
            return Shift.objects.get(id=pk)
        except Shift.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        shift = self.get_object(pk)
        serializer = ShiftListSerializer(shift)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        shift = self.get_object(pk)
        serializer = ShiftSerializer(shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        shift = self.get_object(pk)
        shift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ================================== 6. Books =====================

class BooksView(APIView):
    """ A class to create api for Books """

    def post(self, request, formate=None, **kwargs):
        """creating Books object"""
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None, **kwargs):
        """ showing a list of Books objects"""

        try:
            class_id = self.kwargs["class_id"]
            books = Books.objects.filter(madrasha__slug=madrasha_slug, madrasha_class__id=class_id)
        except:
            books = Books.objects.filter(madrasha__slug=madrasha_slug)
        serializer = BooksListSerializer(books, many=True)
        return Response(serializer.data)


class BooksDetailview(APIView):
    """ Books detail, update and delete"""

    def get_object(self, pk):
        """get single Books obj"""

        try:
            return Books.objects.get(id=pk)
        except Books.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        books = self.get_object(pk)
        serializer = BooksListSerializer(books)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        book = self.get_object(pk)
        serializer = BooksSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ======================= 7. FeesCategory ===============
class FeesCategoryView(APIView):
    def post(self, request, madrasha_slug, formate=None):
        serializer = FeesCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "data": serializer.data, "message": "Fess Category has been created"})
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None):
        obj = FeesCategory.objects.filter(madrash__slug=madrasha_slug)
        serializer = FeesCategoryListSerializer(obj, many=True)
        return Response(serializer.data)


class FeeCategoryDetailView(APIView):
    def get_object(self, pk):
        """get single Books obj"""

        try:
            return FeesCategory.objects.get(id=pk)
        except FeesCategory.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        obj = self.get_object(pk)
        serializer = FeesCategoryListSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        obj = self.get_object(pk)
        serializer = FeesCategorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ================================== 8. Fees =====================
class FeesView(APIView):
    """ A class to create api for Fees """

    def post(self, request, formate=None, **kwargs):
        """creating Fees object"""
        serializer = FeesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None):
        """ showing a list of Fees objects"""
        fees = Fees.objects.filter(madrasha__slug=madrasha_slug)
        serializer = FeesListSerializer(fees, many=True)
        return Response(serializer.data)


class FeesViewByClass(APIView):
    def get(self, request, madrasha_slug, class_id, formate=None):
        """ showing a list of Fees objects"""
        fees = Fees.objects.filter(madrasha__slug=madrasha_slug, madrasha_class__id=class_id)
        serializer = FeesListSerializer(fees, many=True)
        return Response(serializer.data)


class FeesDetailview(APIView):
    """ Fees detail, update and delete"""

    def get_object(self, pk):
        """get single Fees obj"""

        try:
            return Fees.objects.get(id=pk)
        except Fees.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        fee = self.get_object(pk)
        serializer = FeesListSerializer(fee)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        fee = self.get_object(pk)
        serializer = FeesSerializer(fee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        fee = self.get_object(pk)
        fee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ================================== 9. Session =====================

class SessionView(APIView):
    """ A class to create api for Session """

    def post(self, request, formate=None, **kwargs):
        """creating Session object"""
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, madrasha_slug, formate=None):
        """ showing a list of Session objects"""
        session = Session.objects.filter(madrasha__slug=madrasha_slug)
        serializer = SessionListSerializer(session, many=True)
        return Response(serializer.data)


class SessionDetailview(APIView):
    """ Session detail, update and delete"""

    def get_object(self, pk):
        """get single Session obj"""

        try:
            return Session.objects.get(id=pk)
        except Session.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        session = self.get_object(pk)
        serializer = SessionListSerializer(session)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        session = self.get_object(pk)
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        session = self.get_object(pk)
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ================================== 10. Exam rules =====================

class ExamRulesView(APIView):
    """ A class to create api for Session """

    def post(self, request, formate=None):
        """creating Session object"""
        serializer = ExamRulesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, formate=None):
        """ showing a list of Session objects"""
        exam_rules = ExamRules.objects.all()
        serializer = ExamRulesSerializer(exam_rules, many=True)
        return Response(serializer.data)


class ExamRulesDetailview(APIView):
    """ Session detail, update and delete"""

    def get_object(self, pk):
        """get single Session obj"""

        try:
            return ExamRules.objects.get(id=pk)
        except ExamRules.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        exam_rule = self.get_object(pk)
        serializer = ExamRulesSerializer(exam_rule)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        exam_rule = self.get_object(pk)
        serializer = ExamRulesSerializer(exam_rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        exam_rule = self.get_object(pk)
        exam_rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============== 11. Buidling =========================
class BuildingView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Building.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BuildingListSerializer
        return BuildingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BuildingDetailView(APIView):
    """ Session detail, update and delete"""

    def get_object(self, pk):
        """get single Session obj"""

        try:
            return Building.objects.get(id=pk)
        except Building.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        building = self.get_object(pk)
        serializer = BuildingListSerializer(building)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        building = self.get_object(pk)
        serializer = BuildingSerializer(building, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        building = self.get_object(pk)
        building.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============== 12. Room =========================
class RoomView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Room.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoomListSerializer
        return RoomsSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RoomListOnBuilding(APIView):
    def get(self, request, madrasha_slug, building_id, formate=None):
        rooms = Room.objects.filter(madrasha__slug=madrasha_slug, building__id=building_id)
        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data)


class RoomDetailView(APIView):
    """ Session detail, update and delete"""

    def get_object(self, pk):
        """get single Session obj"""

        try:
            return Room.objects.get(id=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        room = self.get_object(pk)
        serializer = RoomListSerializer(room)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        room = self.get_object(pk)
        serializer = RoomsSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        room = self.get_object(pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============== 13. Seat =========================
class SeatView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Seat.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        room_id = self.kwargs['room_id']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug, room__id=room_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SeatListSerializer
        return SeatSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SeatDetailView(APIView):
    """Seat detail, update and delete. """

    def get_object(self, pk):
        """get single Session obj"""

        try:
            return Seat.objects.get(id=pk)
        except Seat.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        """details veiw for single obj"""
        seat = self.get_object(pk)
        serializer = SeatListSerializer(seat)
        return Response(serializer.data)

    def put(self, request, pk, formate=None):
        """update view"""
        seat = self.get_object(pk)
        serializer = SeatSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        """ delete """
        seat = self.get_object(pk)
        seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

##=============== SMS SEND =======================

def SendSMS(numbers, msg):
    apiEndpoint = settings.SMS_API_ENDPOINT
    apiKey = settings.SMS_API_KEY
    apiSender = settings.SMS_SENDER

    headers = {'content-type': 'application/json'}
    url = apiEndpoint
    params = {'apikey': apiKey, 'sender': apiSender,'msisdn': numbers,'smstext':msg}
    response = requests.post(url, params=params, headers=headers)
    return response

class SmsSendView(APIView):
     def post(self, request, formate=None, **kwargs):
        requested_data=request.data
        if (requested_data["numbers"]):
            numbers = requested_data["numbers"]
            msg = requested_data["msg"]
            send_sms = SendSMS(numbers,msg)
            return Response({'message': "Success",'status': True,'data':send_sms})
        else:
            return Response({'message': "Error", 'status':False})
