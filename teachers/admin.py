from django.contrib import admin
from .models import Teacher, Education, Skill


admin.site.register(Education)
admin.site.register(Skill)


@admin.register(Teacher)
class TeacherAdminView(admin.ModelAdmin):
    list_display = ['teacher_id', 'slug']
