from django.contrib import admin
from talimats.models import (
    BookDistributeToTeacher,
    Dawah,
    ExtraActivity,
    ExamAnnouncement,
    ExamRegistration,
    ExamTerm,
    HallDuty,
    ExamRoutine,
    TeacherTraining,
    Syllabus,
    TeacherStaffResponsibility,
    AcademicCalendar,
    ResultInfo,
    SubjectMark, ExamDate
)


# Register your models here.
@admin.register(BookDistributeToTeacher)
class BookDistributeToTeacherAdminView(admin.ModelAdmin):
    list_display = ['kitab_name', 'teacher_name', 'madrasha', 'class_name', 'class_time']


admin.site.register(TeacherTraining)
admin.site.register(Syllabus)
admin.site.register(TeacherStaffResponsibility)
admin.site.register(AcademicCalendar)


@admin.register(Dawah)
class DawahAdminView(admin.ModelAdmin):
    list_display = ['program_name', 'duration', 'start_time', 'managed_by']


@admin.register(ExtraActivity)
class ExtraActivityView(admin.ModelAdmin):
    list_display = ['category', 'duration', 'start_time', 'managed_by']

admin.site.register(ExamAnnouncement)
admin.site.register(ExamRegistration)
admin.site.register(ExamTerm)
admin.site.register(HallDuty)
admin.site.register(ExamRoutine)
admin.site.register(ExamDate)
admin.site.register(ResultInfo)
admin.site.register(SubjectMark)

