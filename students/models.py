import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from teachers.models import RELIGION_CHOICE, GENDER_CHOICE, NATIONALITY_CHOICE
from accounts.models import Address, Madrasha
from settingapp.models import *
from datetime import date

from transactions.models import StudentIncome

# Create your models here.
User = get_user_model()
OCCUPATION_CHOICE = (
    ('null', ''),
    ('teacher', 'Teacher'),
    ('alim', 'Alim'),
    ('farmer', 'Farmer'),
    ('doctor', 'Doctor'),
    ('police', 'Police'),
    ('businessman', 'Businessman'),
    ('govt-employee', 'Govt. employee'),
    ('non-govt-employee', 'Non govt. employee'),
    ('govt-employee', 'Govt. employee'),
    ('house-wife', 'House Wife'),
    ('other', 'Other'),
)
EDUCATION_CHOICE = (
    ('literate', 'Literate'),
    ('ssc/equivalent', 'SSC/equivalent'),
    ('hsc/equivalent', 'HSC/equivalent'),
    ('hons/equivalent', 'Hons/equivalent'),
    ('ma/equivalent', 'M.A./equivalent'),
    ('higher/equivalent', 'Higher/equivalent')
)

RELATION_CHOICE = (
    ('null', ''),
    ('father', 'Father'),
    ('mother', 'Mother'),
    ('brother', 'Brother'),
    ('sister', 'Sister'),
    ('uncle', 'Uncle'),
    ('aunty', 'Aunty'),
    ('cousin', 'Cousin')
)
BOARD_EXAM_CHOICE = (
    ('null', ''),
    ('haya', 'Al Haiatul Ulya'),
    ('befak_arabia', 'Befaq(Arabia)'),
    ('befak_dinia', 'Befaq(Dinia)'),
    ('tanjimul madares', 'Tanjimul Madares')
)


class AcademicFess(models.Model):
    food_bill_percent = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_tution_percent = models.DecimalField(max_digits=10, decimal_places=2)
    scholarship_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Parent(models.Model):
    parent_name = models.CharField(max_length=150, blank=True, null=True)
    parent_date_of_birth = models.DateField(blank=True, null=True)
    parent_nid = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=50, default='null', choices=OCCUPATION_CHOICE)
    organization_with_designation = models.CharField(max_length=255, blank=True, null=True)
    education = models.CharField(max_length=200, default='literate', choices=EDUCATION_CHOICE)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    parent_email = models.EmailField(blank=True, null=True)


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_students', null=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.SET_NULL, related_name='madrasha_students', null=True)
    student_id = models.CharField(max_length=255, blank=True, null=True)
    student_roll_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    date_of_birth = models.DateField()
    age = models.CharField(max_length=255, blank=True, null=True)  # autogenerated from date of birth
    birth_certificate = models.CharField(max_length=255, blank=True, null=True)
    student_nid = models.CharField(max_length=255, blank=True, null=True)
    passport_number = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=20, default='bangladeshi', choices=NATIONALITY_CHOICE, blank=True,
                                   null=True)
    religion = models.CharField(max_length=20, default='islam', choices=RELIGION_CHOICE, blank=True, null=True)
    gender = models.CharField(max_length=20, default='male', choices=GENDER_CHOICE, blank=True, null=True)
    present_address = models.OneToOneField(Address, on_delete=models.SET_NULL, related_name='student_present_addres',
                                           blank=True, null=True)
    permanent_address = models.OneToOneField(Address, on_delete=models.SET_NULL,
                                             related_name='student_permanent_addres', blank=True, null=True)
    father_info = models.OneToOneField(Parent, on_delete=models.SET_NULL, related_name='student_father', blank=True,
                                       null=True)
    mother_info = models.OneToOneField(Parent, on_delete=models.SET_NULL, related_name='student_mother', blank=True,
                                       null=True)

    guardian_name = models.CharField(max_length=150, blank=True, null=True)
    guardian_relation = models.CharField(max_length=20, default='null', choices=RELATION_CHOICE, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=20, default='null', choices=OCCUPATION_CHOICE, blank=True,
                                           null=True)
    yearly_income = models.CharField(max_length=255, blank=True, null=True)
    guardian_contact = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)

    other_contact_person = models.CharField(max_length=150, blank=True, null=True)
    other_contact_person_relation = models.CharField(max_length=20, choices=RELATION_CHOICE, blank=True, null=True)
    other_contact_person_contact = models.CharField(max_length=15, blank=True, null=True)

    sibling_id = models.CharField(max_length=50, blank=True, null=True)
    previous_institution_name = models.CharField(max_length=255, blank=True, null=True)
    previous_institution_contact = models.CharField(max_length=15, blank=True, null=True)
    previous_started_at = models.DateField(blank=True, null=True)
    previous_ending_at = models.DateField(blank=True, null=True)
    previous_ending_class = models.CharField(max_length=50, blank=True, null=True)
    previous_ending_result = models.CharField(max_length=20, blank=True, null=True)
    previous_exam_institute = models.CharField(max_length=300, blank=True, null=True)
    previous_institution_session = models.CharField(max_length=300, blank=True, null=True)
    board_exam_name = models.CharField(max_length=30, default='null', choices=BOARD_EXAM_CHOICE, blank=True, null=True)
    board_exam_registration = models.CharField(max_length=50, blank=True, null=True)
    board_exam_roll = models.CharField(max_length=50, blank=True, null=True)
    board_exam_result = models.CharField(max_length=50, blank=True, null=True)

    admitted_department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='department_students',
                                            blank=True, null=True)
    admitted_class = models.ForeignKey(MadrashaClasses, on_delete=models.SET_NULL, related_name='class_students',
                                       blank=True, null=True)
    admitted_group = models.ForeignKey(MadrashaGroup, on_delete=models.SET_NULL, related_name='group_students',
                                       blank=True, null=True)
    admitted_shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, related_name='shift_students', blank=True,
                                       null=True)

    admitted_roll = models.CharField(max_length=20, blank=True, null=True)
    admitted_session = models.ForeignKey(Session, on_delete=models.SET_NULL, related_name='session_students',
                                         blank=True, null=True)

    student_blood_group = models.CharField(max_length=20, blank=True, null=True)
    special_body_sign = models.CharField(max_length=255, blank=True, null=True)
    # academic_fees = models.ForeignKey(AcademicFess, on_delete=models.SET_NULL, related_name='student_fees_info', blank=True, null=True)
    academic_fees = models.CharField(max_length=255, blank=True, null=True)
    monthly_tution_fee = models.CharField(max_length=50, blank=True, null=True)
    boarding_feee = models.CharField(max_length=50, blank=True, null=True)
    admission_fee = models.CharField(max_length=50, blank=True, null=True)
    transport_fee = models.CharField(max_length=50, blank=True, null=True)
    tution_fee_active_from = models.DateField(blank=True, null=True)
    boarding_fee_active_from = models.DateField(blank=True, null=True)
    transport_fee_active_from = models.DateField(blank=True, null=True)
    is_tution_fee = models.BooleanField(default=False)
    is_boarding_fee = models.BooleanField(default=False)
    is_transport_fee = models.BooleanField(default=False)
    talimi_murobbi_name = models.CharField(max_length=150, blank=True, null=True)
    eslahi_murobbi_name = models.CharField(max_length=150, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        # unique_together = [['student_id', 'madrasha']]
        ordering = ['-slug']

    def generate_student_id(self):
        madrasha_slug = Madrasha.objects.get(id=self.madrasha.id).slug
        starting_from = 100
        last_student = Student.objects.filter(madrasha__slug=madrasha_slug).first()
        if last_student:
            last_student_id_str = last_student.student_id
            slice_it = last_student_id_str[7:]
            last_student_id = int(slice_it)
        else:
            last_student_id = starting_from

        new_student_id = str(last_student_id + 1)
        generated_id = 'S' + madrasha_slug + new_student_id
        print("generated_id", generated_id)
        return generated_id

    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = self.generate_student_id()
        if not self.slug:
            self.slug = self.student_id
        super().save(*args, **kwargs)


class FessInfo(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='madrasha_student_fees_info')
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    student_income = models.ForeignKey(StudentIncome, on_delete=models.PROTECT, blank=True, null=True)
    current_fee = models.IntegerField(blank=True, null=True)
    fees_type = models.CharField(max_length=255, blank=True, null=True)
    for_month = models.CharField(max_length=100, blank=True, null=True)
    fees_type_term = models.CharField(max_length=255, blank=True, null=True)
    paid_amount = models.IntegerField(blank=True, null=True)
    paid_date = models.DateField(default=date.today)

    def __str__(self):
        return self.fees_type


class MealInfo(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='meal_info_madrashas')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='meal_info_student')
    is_breakfast = models.BooleanField(default=False)
    is_lunch = models.BooleanField(default=False)
    is_snacks = models.BooleanField(default=False)
    is_dinner = models.BooleanField(default=False)
    meal_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="meail_info_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['student', 'meal_date']]

    def __str__(self):
        return self.student.student_id
