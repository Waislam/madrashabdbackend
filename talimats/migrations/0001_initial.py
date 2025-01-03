# Generated by Django 4.1.2 on 2023-01-02 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settingapp', '0001_initial'),
        ('accounts', '0001_initial'),
        ('students', '0001_initial'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_start_date_time', models.DateTimeField()),
                ('exam_finish_date_time', models.DateTimeField()),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.madrasha')),
            ],
        ),
        migrations.CreateModel(
            name='ExamTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term_name', models.CharField(max_length=100)),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_term_madrasha', to='accounts.madrasha')),
            ],
            options={
                'unique_together': {('term_name', 'madrasha')},
            },
        ),
        migrations.CreateModel(
            name='ResultInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_marks', models.DecimalField(blank=True, decimal_places=3, default=0.0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_info_exam_term', to='talimats.examterm')),
                ('exam_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_info_session', to='settingapp.session')),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_info_madrasha', to='accounts.madrasha')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='result_info_student', to='students.student')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_info_class', to='settingapp.madrashaclasses')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_title', models.CharField(max_length=255)),
                ('training_description', models.TextField()),
                ('madrasha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='teacher_training', to='accounts.madrasha')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherStaffResponsibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsibility', models.CharField(max_length=500)),
                ('madrasha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='staff_responsibility', to='accounts.madrasha')),
                ('teacher_staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsible_staffs', to='teachers.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_year', models.CharField(max_length=20)),
                ('syllabus_details', models.TextField()),
                ('syllabus_file', models.FileField(blank=True, null=True, upload_to='syllabus')),
                ('exam_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus_term', to='talimats.examterm')),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='syllabus_madrasha', to='accounts.madrasha')),
                ('madrasha_class', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='syllabus_class', to='settingapp.madrashaclasses')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_exam_term', to='talimats.examterm')),
                ('exam_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_mark_session', to='settingapp.session')),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_mark_madrasha', to='accounts.madrasha')),
                ('result_info', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subject_mark_result_info', to='talimats.resultinfo')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subject_mark_student', to='students.student')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_mark_class', to='settingapp.madrashaclasses')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_mark_books', to='settingapp.books')),
            ],
        ),
        migrations.CreateModel(
            name='HallDuty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duty_date', models.DateTimeField(blank=True, null=True)),
                ('date', models.DateField(default=None, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('chief_of_hall', models.CharField(max_length=255)),
                ('assistant_of_hall', models.CharField(blank=True, max_length=255, null=True)),
                ('room_no', models.CharField(max_length=100)),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hall_duty_madrasha', to='accounts.madrasha')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=250)),
                ('duration', models.CharField(max_length=250)),
                ('start_time', models.CharField(max_length=250)),
                ('place', models.CharField(max_length=250)),
                ('date', models.CharField(max_length=250)),
                ('managed_by', models.CharField(max_length=250)),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.madrasha')),
            ],
        ),
        migrations.CreateModel(
            name='ExamRoutine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_exams', to='talimats.examdate')),
                ('exam_subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='routines_books', to='settingapp.books')),
                ('routine_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_routine_class', to='settingapp.madrashaclasses')),
            ],
        ),
        migrations.CreateModel(
            name='ExamRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.TextField(max_length=300)),
                ('is_registered', models.BooleanField(default=False)),
                ('exam_term', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registration_exam_term', to='talimats.examterm')),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exam_registration_madrasha', to='accounts.madrasha')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_session', to='settingapp.session')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exam_registration_student', to='students.student')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_class', to='settingapp.madrashaclasses')),
            ],
        ),
        migrations.AddField(
            model_name='examdate',
            name='routine_term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='routines_terms', to='talimats.examterm'),
        ),
        migrations.CreateModel(
            name='ExamAnnouncement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_title', models.CharField(max_length=255)),
                ('exam_description', models.TextField()),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='exam_announcement', to='accounts.madrasha')),
            ],
        ),
        migrations.CreateModel(
            name='Dawah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=250)),
                ('duration', models.CharField(max_length=250)),
                ('start_time', models.CharField(max_length=250)),
                ('place', models.CharField(max_length=250)),
                ('date', models.CharField(max_length=250)),
                ('managed_by', models.CharField(max_length=250)),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.madrasha')),
            ],
        ),
        migrations.CreateModel(
            name='BookDistributeToTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(max_length=255)),
                ('kitab_name', models.CharField(max_length=255)),
                ('class_time', models.TimeField()),
                ('end_time', models.TimeField(default=None, null=True)),
                ('class_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_to_class', to='settingapp.madrashaclasses')),
                ('madrasha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books_to_teacher', to='accounts.madrasha')),
            ],
        ),
        migrations.CreateModel(
            name='AcademicCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_date', models.DateTimeField()),
                ('description', models.CharField(max_length=500)),
                ('is_leave', models.BooleanField(default=False)),
                ('is_program', models.BooleanField(default=False)),
                ('is_exam', models.BooleanField(default=False)),
                ('other', models.BooleanField(default=False)),
                ('madrasha', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='madrasha_calendar', to='accounts.madrasha')),
            ],
        ),
    ]
