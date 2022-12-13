from django.db import models
from accounts.models import Madrasha
# from students.models import Student


class Department(models.Model):
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_departments')

    class Meta:
        unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.name + " " + self.madrasha.name


class Designation(models.Model):
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_designations')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_designations',
                                   blank=True, null=True)

    class Meta:
        unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.name


class MadrashaClasses(models.Model):
    name = models.CharField(max_length=150, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_classes')
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_classes')

    class Meta:
        unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.name


class MadrashaGroup(models.Model):
    name = models.CharField(max_length=150, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_madrasha_group')
    madrasha_class = models.ForeignKey(MadrashaClasses, on_delete=models.PROTECT, related_name='class_madrasha_group')
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_groups')

    class Meta:
        unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.name


class Shift(models.Model):
    name = models.CharField(max_length=150)
    shift_time = models.TimeField()  # look at this carefully
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_shifts')
    madrasha_class = models.ForeignKey(MadrashaClasses, on_delete=models.PROTECT, related_name='class_shifts')
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_shift')

    class Meta:
        unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.name


class Books(models.Model):
    name = models.CharField(max_length=150, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_books')
    madrasha_class = models.ForeignKey(MadrashaClasses, on_delete=models.PROTECT, related_name='class_books')
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_books')

    class Meta:
        unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=150, blank=True)
    actual_year = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_sessions')

    class Meta:
        unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.actual_year


class FeesCategory(models.Model):
    category_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.category_name


class Fees(models.Model):
    name = models.CharField(max_length=150, blank=True)
    # category = models.ForeignKey(FeesCategory, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='department_fees')
    madrasha_class = models.ForeignKey(MadrashaClasses, on_delete=models.PROTECT, related_name='class_fees')
    amount = models.FloatField()
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_fees')

    class Meta:
        # unique_together = [['name', 'madrasha']]
        ordering = ['name']

    def __str__(self):
        return self.name


class ExamRules(models.Model):
    text_input = models.TextField(max_length=2000)
    is_active = models.BooleanField(default=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_exam_rules')

    def __str__(self):
        return self.text_input


class AdmitCardInfo(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='exam_admit_info')
    talimat_name = models.CharField(max_length=255)
    center_name = models.CharField(max_length=300)

    def __str__(self):
        return self.madrasha.name


class Building(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_buildings')
    building_name = models.CharField(max_length=255)
    total_floor = models.CharField(max_length=10)
    total_room = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.building_name


class Room(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_rooms')
    room_name = models.CharField(max_length=255)
    total_seat = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='building_rooms')
    floor = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.floor + "_" + self.room_name


class Seat(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_seats')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms_seats')
    seat_number = models.IntegerField()
    student = models.OneToOneField('students.student', on_delete=models.SET_NULL, related_name='student_seat', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.seat_number)


# =================== KhabarTakingGroup ================
class KhabarTakingGroup(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_khabar_dist_group')
    # class_of_group = models.One(MadrashaClasses, on_delete=models.CASCADE, related_name='khabar_groups_of_class')
