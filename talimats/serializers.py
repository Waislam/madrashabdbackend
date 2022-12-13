"""
1. BookDistribtuinToTeacherSerializer
2. TeacherTrainingSerializer
3. SyllabusSerializer
4. TeacherStaffResponsibilitySerializer
9. ResultSerializer
16. DawahSerializer
17. ExtraActivitySerializer
"""
from rest_framework import serializers
from talimats.models import (
    BookDistributeToTeacher,
    TeacherTraining,
    Syllabus,
    ExamTerm,
    ExamAnnouncement,
    ExamRegistration,
    HallDuty,
    TeacherStaffResponsibility,
    Dawah,
    ExtraActivity,
    ExamRoutine, SubjectMark, ResultInfo, ExamDate
)


# ==================== 1. BookDistribtuinToTeacherSerializer ============================== #
class BookDistributionToTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDistributeToTeacher
        fields = '__all__'


class BookDistributionToTeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDistributeToTeacher
        fields = '__all__'
        depth = 2


# ==================== 2. TeacherTrainingSerializer ============================== #
class TeacherTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherTraining
        fields = '__all__'


class TeacherTrainingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherTraining
        fields = '__all__'
        depth = 2


# ==================== 3. SyllabusSerializer ============================== #
class ExamTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTerm
        fields = '__all__'


class SyllabusSerializer(serializers.ModelSerializer):
    exam_term = ExamTermSerializer()

    class Meta:
        model = Syllabus
        fields = ['id', 'madrasha', 'madrasha_class', 'exam_term', 'session_year', 'syllabus_details', 'syllabus_file']

    def create(self, validated_data):
        exam_term = validated_data.pop('exam_term')
        exam_term_obj = ExamTerm.objects.create(**exam_term)

        syllabus = Syllabus.objects.create(exam_term=exam_term_obj, **validated_data)
        return syllabus

    def update(self, instance, validated_data):
        exam_term_instance = instance.exam_term
        exam_term_instance.term_name = validated_data.get('exam_term').get('term_name', exam_term_instance.term_name)
        exam_term_instance.save()

        instance.madrasha_class = validated_data.get('madrasha_class', instance.madrasha_class)
        instance.session_year = validated_data.get('session_year', instance.session_year)
        instance.syllabus_details = validated_data.get('syllabus_details', instance.syllabus_details)
        instance.syllabus_file = validated_data.get('syllabus_file', instance.syllabus_file)
        instance.save()
        return instance


class SyllabusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = '__all__'
        depth = 2


# ==================== 4. TeacherStaffResponsibilitySerializer ============================== #
class TeacherStaffResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherStaffResponsibility
        fields = '__all__'


class TeacherStaffResponsibilityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherStaffResponsibility
        fields = '__all__'
        depth = 2


# ==================== 16. DawahSerializer ============================== #
class DawahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dawah
        fields = '__all__'


class DawahListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dawah
        fields = '__all__'
        depth = 2


# ==================== 17. ExtraActivitySerializer ============================== #
class ExtraActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraActivity
        fields = '__all__'


class ExtraActivityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraActivity
        fields = '__all__'
        depth = 2


class ExamAnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAnnouncement
        fields = '__all__'
        depth = 2


class ExamAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAnnouncement
        fields = '__all__'


class ExamRegistrationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        fields = '__all__'
        depth = 2


class ExamRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRegistration
        fields = '__all__'


class ExamTermListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamTerm
        fields = '__all__'


class HallDutySerializer(serializers.ModelSerializer):
    class Meta:
        model = HallDuty
        fields = '__all__'


# ========== exam routine section ==================
class ExamRoutineSerializer(serializers.ModelSerializer):
    # exam_date = ExamDateSerializer()
    class Meta:
        model = ExamRoutine
        fields = '__all__'


class ExamRoutineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRoutine
        fields = '__all__'
        # depth = 2


class ExamDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamDate
        fields = '__all__'


class ExamDateListSerializer(serializers.ModelSerializer):
    exam_routine = ExamRoutineListSerializer(read_only=True, many=True)

    class Meta:
        model = ExamDate
        fields = ['id', 'madrasha', 'exam_start_date_time', 'exam_finish_date_time', 'exam_routine', 'routine_term']
        # depth = 2


# ========================= 9. ResultSerializer ===============
class ClassResultFileUploadSerializer(serializers.Serializer):
    madrasha = serializers.CharField()
    student = serializers.CharField()
    student_class = serializers.CharField()
    exam_term = serializers.CharField()
    subject = serializers.CharField()
    year = serializers.CharField()
    file = serializers.FileField()

    class Meta:
        fields = ('file',)


class ResultInfoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultInfo
        fields = '__all__'
        depth = 2


class SubjectMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectMark
        fields = '__all__'
        depth = 2
