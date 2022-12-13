from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import Address, Madrasha
from settingapp.models import Department, Designation
from django.template.defaultfilters import slugify
from datetime import datetime, date
# Create your models here.

# User = settings.AUTH_USER_MODEL
User = get_user_model()

GENDER_CHOICE = (
    ('male', 'Male'),
    ('female', 'Female')
)
RELIGION_CHOICE = (
    ('islam', 'Islam'),
    ('shonaton', 'Shonaton'),
    ('other', 'Other')
)
MARITAL_STATUS = (
    ('married', 'Married'),
    ('unmarried', 'Unmarried')
)
NATIONALITY_CHOICE = (
    ('bangladeshi', 'Bangladeshi'),
    ('indian', 'Indian'),
    ('other', 'Other')
)


class Education(models.Model):
    degree_name = models.CharField(max_length=255, blank=True, null=True)
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    passing_year = models.CharField(max_length=255, blank=True, null=True)
    result = models.CharField(max_length=255, blank=True, null=True)

    # def __str__(self):
    #     return self.degree_name


class Skill(models.Model):
    skill_name = models.CharField(max_length=255, blank=True, null=True)

    # def __str__(self):
    #     return self.skill_name


class Experience(models.Model):
    experience_name = models.CharField(max_length=255, blank=True, null=True)

    # def __str__(self):
    #     return self.experience_name


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='teachers', blank=True, null=True)
    madrasha = models.ForeignKey(Madrasha, on_delete=models.SET_NULL, related_name='madrasha_teachers', null=True)
    teacher_id = models.CharField(max_length=20, unique=True, blank=True)  # auto incremented and generated
    father_name = models.CharField(max_length=150, blank=True, null=True)
    mother_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, default='male', choices=GENDER_CHOICE, blank=True, null=True)
    religion = models.CharField(max_length=20, default='islam', choices=RELIGION_CHOICE, blank=True, null=True)
    marital_status = models.CharField(max_length=15, default='married', choices=MARITAL_STATUS, blank=True, null=True)
    present_address = models.OneToOneField(Address, on_delete=models.SET_NULL, related_name='present_addres', blank=True, null=True)
    permanent_address = models.OneToOneField(Address, on_delete=models.SET_NULL, related_name='permanent_addres', blank=True, null=True)
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='teacher_educations')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='teacher_skills', blank=True, null=True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='teacher_experience', blank=True, null=True)
    phone_home = models.CharField(max_length=15, blank=True, null=True)
    nid = models.CharField(max_length=200)
    birth_certificate = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=20, default='bangladeshi', choices=NATIONALITY_CHOICE)
    blood_group = models.CharField(max_length=15, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='department_teachers', blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, related_name='designated_teachers', blank=True, null=True)
    starting_date = models.DateField(default=date.today)
    ending_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def generate_teacher_id(self):
        starting_from = 100
        last_teacher = Teacher.objects.last()
        if last_teacher:
            last_teacher_id_str = last_teacher.teacher_id
            slice_it = last_teacher_id_str[1:]
            last_teacher_id = int(slice_it)
        else:
            last_teacher_id = starting_from

        new_teacher_id = str(last_teacher_id + 1)
        generated_id = 'T' + new_teacher_id
        return generated_id

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            self.teacher_id = self.generate_teacher_id()
        if not self.slug:
            self.slug = slugify(self.teacher_id)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.teacher_id

