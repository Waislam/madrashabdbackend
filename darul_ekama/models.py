from django.db import models
from accounts.models import Madrasha
from settingapp.models import Building, Room, Seat, MadrashaClasses
from students.models import Student
from teachers.models import Teacher


# Create your models here.

class SeatBooking(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_seat_booking')
    students = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_seat_dist')
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, related_name='building_seats', blank=True,
                                 null=True)
    floor = models.CharField(max_length=3)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name='room_seats', blank=True, null=True)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, related_name='booked_seat', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.seat.seat_number)


class NigraniTable(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_darul_ekam_nigrani')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='teacher_nigrani', blank=True,
                                null=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, related_name='building_nigrans', blank=True,
                                 null=True)
    floor = models.CharField(max_length=20)
    room = models.ManyToManyField(Room, related_name='room_nigran', blank=True)
    class_nigran = models.ForeignKey(MadrashaClasses, on_delete=models.SET_NULL, related_name='class_nigrans',
                                     blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.teacher.teacher_id
