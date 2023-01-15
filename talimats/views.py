"""
1. Book Distribution to teacher view
2. Teacher Training View
3. Syllabus View
"""
import csv
import io

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins, generics, status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import Madrasha
from students.models import Student
from talimats.models import (
    BookDistributeToTeacher,
    TeacherTraining,
    Syllabus,
    ExamAnnouncement,
    ExamRegistration,
    ExamTerm,
    HallDuty,
    TeacherStaffResponsibility,
    Dawah,
    ExtraActivity,
    ExamRoutine,
    SubjectMark,
    ResultInfo, ExamDate
)
from rest_framework.response import Response
from talimats.serializers import (
    BookDistributionToTeacherSerializer,
    TeacherTrainingSerializer,
    SyllabusSerializer,
    ExamAnnouncementListSerializer,
    ExamAnnouncementSerializer,
    ExamRegistrationListSerializer,
    ExamRegistrationSerializer,
    ExamTermSerializer,
    HallDutySerializer,
    TeacherStaffResponsibilitySerializer,
    DawahSerializer,
    ExtraActivitySerializer,
    ExamRoutineSerializer,
    BookDistributionToTeacherListSerializer,
    SyllabusListSerializer,
    TeacherStaffResponsibilityListSerializer,
    TeacherTrainingListSerializer,
    DawahListSerializer,
    ExtraActivityListSerializer,
    ClassResultFileUploadSerializer,
    SubjectMarkSerializer,
    ExtraActivityListSerializer, ResultInfoListSerializer, ExamRoutineListSerializer, ExamDateSerializer,
    ExamDateListSerializer
)
from core.pagination import CustomPagination
from teachers.models import Teacher


# ====================== 1. Book Distribution to teacher view ================
class BookDistributionToTeacherView(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    generics.GenericAPIView
                                    ):
    queryset = BookDistributeToTeacher.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(BookDistributionToTeacherView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookDistributionToTeacherListSerializer
        return BookDistributionToTeacherSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BookDistToTeacherDetailView(APIView):

    def get_object(self, pk):
        try:
            return BookDistributeToTeacher.objects.get(id=pk)
        except BookDistributeToTeacher.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = BookDistributionToTeacherListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = BookDistributionToTeacherSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Book Distribtuion to teacher has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response({'status': True, "message": "your object has been deleted"})


# ====================== 2. Teacher Training View ================
class TeacherTrainingView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = TeacherTraining.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TeacherTrainingListSerializer
        return TeacherTrainingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TeacherTrainingDetailView(APIView):
    def get_object(self, pk):
        try:
            return TeacherTraining.objects.get(id=pk)
        except TeacherTraining.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = TeacherTrainingListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = TeacherTrainingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Teacher Training notice has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response({'status': True, "message": "your object has been deleted"})


# ====================== 3. Syllabus View ================
class SyllabusView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Syllabus.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SyllabusListSerializer
        return SyllabusSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SyllabusDetailView(APIView):
    def get_object(self, pk):
        try:
            return Syllabus.objects.get(id=pk)
        except Syllabus.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = SyllabusListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = SyllabusSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Syllabus has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response({'status': True, "message": "your object has been deleted"})


# ====================== 4. TeacherStaffResponsibility View ================
class TeacherStaffResponsibilityView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = TeacherStaffResponsibility.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TeacherStaffResponsibilityListSerializer
        return TeacherStaffResponsibilitySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        teacher_id = Teacher.objects.get(teacher_id=request.data["teacher_staff"]).id
        request.data["teacher_staff"] = teacher_id
        return self.create(request, *args, **kwargs)


class TeacherStaffResponsibilityDetailView(APIView):
    def get_object(self, pk):
        try:
            return TeacherStaffResponsibility.objects.get(id=pk)
        except TeacherStaffResponsibility.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = TeacherStaffResponsibilityListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = TeacherStaffResponsibilitySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Object has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response({'status': True, "message": "your object has been deleted"})


# ====================== 16. Dawah view ================
class DawahView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Dawah.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(DawahView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return DawahListSerializer
        return DawahSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DawahDetailView(APIView):

    def get_object(self, pk):
        try:
            return Dawah.objects.get(id=pk)
        except Dawah.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = DawahListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = DawahSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Dawah has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(
            {
                "status": True,
                "message": "Dawah has been successfully Delete",
            }
        )


# ====================== 17. ExtraActivity View ================
class ExtraActivityView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = ExtraActivity.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        return super(ExtraActivityView, self).get_queryset().filter(madrasha__slug=madrasha_slug)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ExtraActivityListSerializer
        return ExtraActivitySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExtraActivityDetailView(APIView):

    def get_object(self, pk):
        try:
            return ExtraActivity.objects.get(id=pk)
        except ExtraActivity.DoesNotExist:
            raise Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = ExtraActivityListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = ExtraActivitySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Extra Activity has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, formate=None):
        obj = self.get_object(pk)
        obj.delete()
        return Response(
            {
                "status": True,
                "message": "Extra activity has been successfully Delete",
            }
        )


class ExamAnnouncementView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ExamAnnouncement.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ExamAnnouncementListSerializer
        return ExamAnnouncementSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExamAnnouncementDetailView(APIView):

    def get_object(self, pk):
        try:
            return ExamAnnouncement.objects.get(id=pk)
        except ExamAnnouncement.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = ExamAnnouncementListSerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = ExamAnnouncementSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Syllabus has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        exam_announcement = self.get_object(pk)
        exam_announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExamRegistrationListView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = ExamRegistration.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['student__student_id']

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ExamRegistrationListSerializer
        return ExamRegistrationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExamTermListView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = ExamTerm.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        return ExamTermSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExamTermDetailsView(APIView):
    def get_object(self, pk):
        try:
            return ExamTerm.objects.get(id=pk)
        except ExamTerm.DoesNotExist:
            return Http404

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = ExamTermSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Exam Term has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class HallDutyListView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = HallDuty.objects.all()

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get_serializer_class(self):
        return HallDutySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class HallNigranDetailView(APIView):

    def get_object(self, pk):
        try:
            return HallDuty.objects.get(id=pk)
        except HallDuty.DoesNotExist:
            return Http404

    def get(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = HallDutySerializer(obj)
        return Response({"status": True, "data": serializer.data})

    def put(self, request, pk, formate=None):
        obj = self.get_object(pk)
        serializer = HallDutySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Syllabus has been updated successfully",
                    "data": serializer.data,
                }
            )
        return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        exam_announcement = self.get_object(pk)
        exam_announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExamRoutineListView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = ExamDate.objects.all()
    serializer_class = ExamDateListSerializer

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class ExamRoutineListView(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = ExamRoutine.objects.all()
#     serializer_class = ExamRoutineListSerializer
#
#     def get_queryset(self):
#         madrasha_slug = self.kwargs['madrasha_slug']
#         queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
#         list_query = []
#         for item in queryset:
#             list_query.append(item.date_exams.all())
#
#         result = ExamDate.objects.filter(pk__in=list_query)
#         print("typeOf", type(result))
#
#         # return list_query
#         return queryset
#
#     # def get_serializer_class(self):
#     #     if self.request.method == "GET":
#     #         return ExamDateListSerializer
#     #     return ExamDateSerializer
#
#     def get(self, request, *args, **kwargs):
#         # for item in self.list:
#         #     print("item: ", item)
#         return self.list(request, *args, **kwargs)

class ExamRoutineCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ExamDate.objects.all()
    serializer_class = ExamRoutineSerializer

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super().get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def post(self, request, *args, **kwargs):
        data = request.data
        madrasha = Madrasha.objects.get(id=data['madrasha'])
        routine_term = ExamTerm.objects.get(id=data['routine_term'])

        obj, created = ExamDate.objects.get_or_create(
            madrasha=madrasha,
            exam_start_date_time=data['exam_start_date_time'],
            exam_finish_date_time=data['exam_finish_date_time'],
            routine_term=routine_term
        )

        data['exam_date'] = obj.id

        return self.create(request, *args, **kwargs)


class UpdateClassResult(generics.CreateAPIView):
    """UpLoading result file and creating Result Info table"""
    serializer_class = ClassResultFileUploadSerializer

    def post(self, request, *args, **kwargs):
        # try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        exam_term = serializer.validated_data['exam_term']
        madrasha = serializer.validated_data['madrasha']
        # student = serializer.validated_data['student']
        student_class = serializer.validated_data['student_class']
        year = serializer.validated_data['year']
        subject = serializer.validated_data['subject']

        decoded_file = file.read().decode()
        # upload_products_csv.delay(decoded_file, request.user.pk)
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        header = next(reader)

        subject_mark = SubjectMark.objects.filter(
            subject=subject,
            madrasha_id=madrasha,
            exam_term_id=exam_term,
            exam_year_id=year,
            student_class_id=student_class,
        ).exists()
        # print("subject_mark exist", subject_mark)

        if subject_mark:
            return Response(
                {
                    "status": False,
                    "msg": "This subject result already exists !!"
                },
                status=status.HTTP_302_FOUND
            )
        else:
            save_result = []
            for row in reader:
                try:
                    print(row[0])
                    student = Student.objects.get(slug=row[0])
                    result_info, _ = ResultInfo.objects.get_or_create(
                        madrasha_id=madrasha,
                        student=student,
                        exam_term_id=exam_term,
                        exam_year_id=year,
                        student_class_id=student_class,
                    )

                    subject_mark = SubjectMark.objects.create(
                        result_info=result_info,
                        madrasha_id=madrasha,
                        student=student,
                        exam_term_id=exam_term,
                        exam_year_id=year,
                        student_class_id=student_class,
                        subject_id=subject,
                        mark=int(row[1])
                    )

                    # all_marks = SubjectMark.objects.filter(
                    #     result_info=result_info,
                    # )
                    #
                    # print(all_marks)

                    result_info.total_marks += int(row[1])
                    result_info.save()

                    save_result.append(subject_mark)
                except:
                    pass

            subject_serailiser = SubjectMarkSerializer(save_result, many=True)
            return Response({"status": True, "save_data_list": subject_serailiser.data}, status=status.HTTP_201_CREATED)


class ResultInfoListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = ResultInfo.objects.all()
    serializer_class = ResultInfoListSerializer

    def get_queryset(self):
        madrasha_slug = self.kwargs['madrasha_slug']
        queryset = super(ResultInfoListView, self).get_queryset().filter(madrasha__slug=madrasha_slug)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubjectMarkView(
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = SubjectMark.objects.all()
    serializer_class = SubjectMarkSerializer

    def get_queryset(self):
        result_info_id = self.kwargs['result_info_id']
        queryset = super().get_queryset().filter(result_info_id=result_info_id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
