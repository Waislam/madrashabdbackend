from rest_framework import serializers
from .models import (Department, Designation, MadrashaClasses,
                     MadrashaGroup, Shift, Session, Books, Fees,
                     ExamRules, Building, Seat, Room, FeesCategory)
from accounts.serializers import MadrashaSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'is_active', 'madrasha')


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'is_active', 'madrasha')
        depth = 2


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ('id', 'name', 'is_active', 'madrasha', 'department')


class DesignationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ('id', 'name', 'is_active', 'madrasha', 'department')
        depth = 2


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MadrashaClasses
        fields = ('id', 'name', 'department', 'is_active', 'madrasha')


class ClassListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MadrashaClasses
        fields = ('id', 'name', 'department', 'is_active', 'madrasha')
        depth = 2


class ClassGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = MadrashaGroup
        fields = ('id', 'name', 'department', 'madrasha_class', 'is_active', 'madrasha')


class ClassGroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MadrashaGroup
        fields = ('id', 'name', 'department', 'madrasha_class', 'is_active', 'madrasha')
        depth = 2


class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift
        fields = ('id', 'name', 'shift_time', 'department', 'madrasha_class', 'is_active', 'madrasha')


class ShiftListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ('id', 'name', 'shift_time', 'department', 'madrasha_class', 'is_active', 'madrasha')
        depth = 2


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'name', 'actual_year', 'is_active', 'madrasha')


class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'name', 'actual_year', 'is_active', 'madrasha')
        depth = 2


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id', 'name', 'department', 'madrasha_class', 'is_active', 'madrasha')


class BooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id', 'name', 'department', 'madrasha_class', 'is_active', 'madrasha')
        depth = 2


class FeesCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FeesCategory
        fields = '__all__'


class FeesCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesCategory
        fields = '__all__'
        depth = 2


class FeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'


class FeesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fees
        fields = '__all__'
        depth = 2


class ExamRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRules
        fields = ('id', 'text_input', 'is_active', 'madrasha')


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"


class BuildingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = "__all__"
        depth = 2


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class SeatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"
        depth = 2


class RoomsSerializer(serializers.ModelSerializer):
    # seats = SeatSerializer()

    class Meta:
        model = Room
        fields = ['id', 'madrasha', 'room_name', 'building', 'total_seat', 'is_active', 'floor']

    def create(self, validated_data):
        room = Room.objects.create(**validated_data)

        total_seat = room.total_seat
        for seat in range(1, total_seat+1):
            seat = Seat.objects.create(madrasha=room.madrasha, seat_number=seat, room=room)
        return room


class RoomListSerializer(serializers.ModelSerializer):
    # seats = SeatSerializer()

    class Meta:
        model = Room
        fields = ['id', 'madrasha', 'room_name', 'building', 'total_seat', 'is_active', 'floor']
        depth = 2
