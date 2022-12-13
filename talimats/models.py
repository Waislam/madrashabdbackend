"""
1. Book Distribution to Teacher
2. TeacherTraining
3. Syllabus Creation
4. TeacherStaffResponsibility
5. AcademicCalendar
6. ExamAnnouncement
7. ExamRegistration
8. ExamRoutine
9. Result Info
10. Result
16. Dawah
18. Dar_ul Ekama
"""

from django.db import models
from accounts.models import Madrasha
from settingapp.models import MadrashaClasses, Books, Session

from teachers.models import Teacher
from students.models import Student


# Create your models here.
# ================== 1. Book Distribution to Teacher ===============#
class BookDistributeToTeacher(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name="books_to_teacher", blank=True,
                                 null=True)
    teacher_name = models.CharField(max_length=255)
    kitab_name = models.CharField(max_length=255)
    class_name = models.ForeignKey(MadrashaClasses, on_delete=models.SET_NULL, related_name="book_to_class", blank=True,
                                   null=True)
    class_time = models.TimeField()
    end_time = models.TimeField(null=True, default=None)

    def __str__(self):
        return self.kitab_name


# ================== 2. TeacherTraining ===============#
class TeacherTraining(models.Model):
    madrasha = models.ForeignKey(
        Madrasha,
        on_delete=models.PROTECT,
        related_name='teacher_training',
        blank=True,
        null=True
    )
    training_title = models.CharField(max_length=255)
    training_description = models.TextField()

    def __str__(self):
        return self.training_title


# ================== 3. Syllabus Creation ===============#
class ExamTerm(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name="exam_term_madrasha")
    term_name = models.CharField(max_length=100)

    class Meta:
        unique_together = [['term_name', 'madrasha']]

    def __str__(self):
        return self.term_name


class Syllabus(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name="syllabus_madrasha")
    madrasha_class = models.ForeignKey(MadrashaClasses, on_delete=models.PROTECT, related_name='syllabus_class')
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE, related_name='syllabus_term')
    session_year = models.CharField(max_length=20)  # read only from anywhere
    syllabus_details = models.TextField()
    syllabus_file = models.FileField(upload_to='syllabus', blank=True, null=True)

    def __str__(self):
        return self.exam_term.term_name


# ================== 4. TeacherStaffResponsibility ===============#
class TeacherStaffResponsibility(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.SET_NULL, related_name="staff_responsibility", null=True,
                                 blank=True)
    teacher_staff = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="responsible_staffs")
    responsibility = models.CharField(max_length=500)

    def __str__(self):
        return self.teacher_staff.teacher_id


# ================== 5. AcademicCalendar ===============#
class AcademicCalendar(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name="madrasha_calendar")
    calendar_date = models.DateTimeField()
    description = models.CharField(max_length=500)
    is_leave = models.BooleanField(default=False)
    is_program = models.BooleanField(default=False)
    is_exam = models.BooleanField(default=False)
    other = models.BooleanField(default=False)

    def __str__(self):
        return str(self.calendar_date)


# ================== 6. ExamAnnouncement ===============#
class ExamAnnouncement(models.Model):
    madrasha = models.ForeignKey(
        Madrasha,
        on_delete=models.PROTECT,
        related_name='exam_announcement'
    )
    exam_title = models.CharField(max_length=255)
    exam_description = models.TextField()

    def __str__(self):
        return self.exam_title


# ================== 7. ExamRegistration ===============#
class ExamRegistration(models.Model):
    madrasha = models.ForeignKey(
        Madrasha,
        on_delete=models.PROTECT,
        related_name='exam_registration_madrasha'
    )
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='exam_registration_student')
    amount = models.TextField(max_length=300)
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.PROTECT, related_name='registration_exam_term')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='registration_session')
    student_class = models.ForeignKey(MadrashaClasses, on_delete=models.CASCADE, related_name='registration_class')
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.student.student_id


# ================== 8. ExamRoutine ===============#
class ExamDate(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT)
    exam_start_date_time = models.DateTimeField()
    exam_finish_date_time = models.DateTimeField()
    routine_term = models.ForeignKey(ExamTerm, on_delete=models.PROTECT, related_name='routines_terms')

    def __str__(self):
        return str(self.exam_start_date_time)


class ExamRoutine(models.Model):
    routine_class = models.ForeignKey(MadrashaClasses, on_delete=models.CASCADE, related_name='exam_routine_class')
    exam_subject = models.ForeignKey(Books, on_delete=models.PROTECT, related_name='routines_books')
    exam_date = models.ForeignKey(ExamDate, on_delete=models.CASCADE, related_name='date_exams')

    def __str__(self):
        return self.routine_class.name


# ================== 9. Result Info ===============#


# ================== 16. Dawah ===============#
class Dawah(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT)
    program_name = models.CharField(max_length=250)
    duration = models.CharField(max_length=250)
    start_time = models.CharField(max_length=250)
    place = models.CharField(max_length=250)
    date = models.CharField(max_length=250)
    managed_by = models.CharField(max_length=250)

    def __str__(self):
        return self.program_name


# ================== 17. Extra Activity ===============#
class ExtraActivity(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT)
    category = models.CharField(max_length=250)
    duration = models.CharField(max_length=250)
    start_time = models.CharField(max_length=250)
    place = models.CharField(max_length=250)
    date = models.CharField(max_length=250)
    managed_by = models.CharField(max_length=250)

    def __str__(self):
        return self.category


class HallDuty(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.PROTECT, related_name='hall_duty_madrasha')
    duty_date = models.DateTimeField(blank=True, null=True)
    date = models.DateField(null=True, default=None)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    chief_of_hall = models.CharField(max_length=255)
    assistant_of_hall = models.CharField(max_length=255, null=True, blank=True)
    room_no = models.CharField(max_length=100)

    def __str__(self):
        return self.room_no


# =============== 18. Dar_ul Ekama ================================


class ResultInfo(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name='result_info_madrasha')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='result_info_student')
    exam_year = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='result_info_session')
    student_class = models.ForeignKey(MadrashaClasses, on_delete=models.CASCADE, related_name='result_info_class')
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE, related_name='result_info_exam_term')
    total_marks = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.student_id


class SubjectMark(models.Model):
    result_info = models.ForeignKey(ResultInfo, on_delete=models.PROTECT, related_name='subject_mark_result_info')
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name='subject_mark_madrasha')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='subject_mark_student')
    exam_year = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='subject_mark_session')
    student_class = models.ForeignKey(MadrashaClasses, on_delete=models.CASCADE, related_name='subject_mark_class')
    exam_term = models.ForeignKey(ExamTerm, on_delete=models.CASCADE, related_name='subject_exam_term')
    subject = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='subject_mark_books')
    mark = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.student_id + "-" + self.subject.name
