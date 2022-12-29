"""
1. address serializer
2. ParentSerializer
3. StudentSerializer
"""

from rest_framework import serializers

from settingapp.serializers import DepartmentSerializer, ClassGroupSerializer, ShiftSerializer, SessionSerializer, \
    ClassSerializer
from .models import Student, AcademicFess, Parent, FessInfo
from accounts.models import Address, CustomUser
from accounts.serializers import AddressSerializer, CustomUserSerializer, AddressDetailSerializer, MadrashaSerializer, \
    CustomUserListSerializer, CustomUserUpdateSerializer


# ================= 2. ParentSerializer =====================


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'parent_name', 'parent_date_of_birth', 'parent_nid', 'occupation',
                  'organization_with_designation',
                  'education', 'contact_number', 'parent_email']


# class EducationSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model =


# ================= 3. StudentSerializer =====================

class AcademicFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicFess
        fields = '__all__'


class StudentListSerializer(serializers.ModelSerializer):
    user = CustomUserListSerializer()

    # madrasha = MadrashaSerializer()
    # present_address = AddressDetailSerializer()
    # permanent_address = AddressDetailSerializer()
    # father_info = ParentSerializer()
    # mother_info = ParentSerializer()
    # admitted_department = DepartmentSerializer()
    # admitted_class = ClassSerializer()
    # admitted_group = ClassGroupSerializer()
    # admitted_shift = ShiftSerializer()
    # admitted_session = SessionSerializer()
    # academic_fees = AcademicFeesSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'madrasha', 'student_id', 'student_roll_id', 'date_of_birth', 'age',
                  'birth_certificate',
                  'student_nid', 'passport_number', 'nationality', 'religion', 'gender', 'present_address',
                  'permanent_address', 'father_info', 'mother_info', 'guardian_name', 'guardian_relation',
                  'guardian_occupation', 'yearly_income', 'guardian_contact',
                  'guardian_email', 'other_contact_person', 'other_contact_person_relation',
                  'other_contact_person_contact', 'sibling_id', 'previous_institution_name',
                  'previous_institution_contact',
                  'previous_started_at', 'previous_ending_at', 'previous_ending_class', 'previous_ending_result',
                  'board_exam_name', 'board_exam_registration', 'board_exam_roll', 'board_exam_result',
                  'admitted_department',
                  'admitted_class', 'admitted_group', 'admitted_shift', 'admitted_roll', 'admitted_session',
                  'student_blood_group', 'special_body_sign', 'academic_fees', 'monthly_tution_fee', 'boarding_feee',
                  'admission_fee', 'transport_fee', 'tution_fee_active_from', 'boarding_fee_active_from',
                  'transport_fee_active_from', 'is_tution_fee', 'is_boarding_fee', 'is_transport_fee',
                  'talimi_murobbi_name', 'eslahi_murobbi_name', 'slug']
        depth = 2


class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    present_address = AddressSerializer()
    permanent_address = AddressSerializer()
    father_info = ParentSerializer()
    mother_info = ParentSerializer()

    # user = serializers.SerializerMethodField("user_first_name")

    class Meta:
        model = Student
        fields = ['id', 'user', 'madrasha', 'student_id', 'student_roll_id', 'date_of_birth', 'age',
                  'birth_certificate',
                  'student_nid',
                  'passport_number', 'nationality', 'religion', 'gender', 'present_address', 'permanent_address',
                  'father_info', 'mother_info', 'guardian_name', 'guardian_relation', 'guardian_occupation',
                  'yearly_income', 'guardian_contact',
                  'guardian_email', 'other_contact_person', 'other_contact_person_relation',
                  'other_contact_person_contact', 'sibling_id', 'previous_institution_name',
                  'previous_institution_contact',
                  'previous_started_at', 'previous_ending_at', 'previous_ending_class', 'previous_ending_result',
                  'board_exam_name', 'board_exam_registration', 'board_exam_roll', 'board_exam_result',
                  'admitted_department',
                  'admitted_class', 'admitted_group', 'admitted_shift', 'admitted_roll', 'admitted_session',
                  'student_blood_group', 'special_body_sign', 'academic_fees', 'monthly_tution_fee', 'boarding_feee',
                  'admission_fee', 'transport_fee', 'tution_fee_active_from', 'boarding_fee_active_from',
                  'transport_fee_active_from', 'is_tution_fee', 'is_boarding_fee', 'is_transport_fee',
                  'talimi_murobbi_name', 'eslahi_murobbi_name', 'slug']

    # def user_first_name(self, obj):
    #     first_name = obj.user.first_name
    #     return first_name

    def create(self, validated_data):
        user_field = validated_data.pop('user')
        present_address = validated_data.pop('present_address')
        permanent_address = validated_data.pop('permanent_address')
        father_info = validated_data.pop('father_info')
        mother_info = validated_data.pop('mother_info')

        # create address object
        present_address_obj = Address.objects.create(**present_address)
        permanent_address_obj = Address.objects.create(**permanent_address)

        # create parents info
        father_info_obj = Parent.objects.create(**father_info)
        mother_info_obj = Parent.objects.create(**mother_info)

        # create custom user
        phone = user_field.pop('phone')

        user_obj = CustomUser.objects.create_user(phone=phone, **user_field)

        student = Student.objects.create(
            user=user_obj,
            present_address=present_address_obj,
            permanent_address=permanent_address_obj,
            father_info=father_info_obj, mother_info=mother_info_obj,
            **validated_data
        )
        return student


class StudentSerializerUpdate(serializers.ModelSerializer):
    """
    This serializer is working to update student without updating user
    """
    user = CustomUserUpdateSerializer()
    present_address = AddressSerializer()
    permanent_address = AddressSerializer()
    father_info = ParentSerializer()
    mother_info = ParentSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'madrasha', 'student_id', 'student_roll_id', 'date_of_birth', 'age',
                  'birth_certificate',
                  'student_nid',
                  'passport_number', 'nationality', 'religion', 'gender', 'present_address', 'permanent_address',
                  'father_info', 'mother_info', 'guardian_name', 'guardian_relation', 'guardian_occupation',
                  'yearly_income', 'guardian_contact',
                  'guardian_email', 'other_contact_person', 'other_contact_person_relation',
                  'other_contact_person_contact', 'sibling_id', 'previous_institution_name',
                  'previous_institution_contact',
                  'previous_started_at', 'previous_ending_at', 'previous_ending_class', 'previous_ending_result',
                  'board_exam_name', 'board_exam_registration', 'board_exam_roll', 'board_exam_result',
                  'admitted_department',
                  'admitted_class', 'admitted_group', 'admitted_shift', 'admitted_roll', 'admitted_session',
                  'student_blood_group', 'special_body_sign', 'academic_fees', 'monthly_tution_fee', 'boarding_feee',
                  'admission_fee', 'transport_fee', 'tution_fee_active_from', 'boarding_fee_active_from',
                  'transport_fee_active_from', 'is_tution_fee', 'is_boarding_fee', 'is_transport_fee',
                  'talimi_murobbi_name', 'eslahi_murobbi_name', 'slug']

    def update(self, instance, validated_data):
        # print("instance detail: ", instance.student_id)

        user = instance.user
        present_address = instance.present_address
        permanent_address = instance.permanent_address
        father_info = instance.father_info
        mother_info = instance.mother_info

        # add new value to the form field
        def address_method(varname, validated_value):
            varname.division = validated_data.get(validated_value).get('division', varname.division)
            varname.district = validated_data.get(validated_value).get('district', varname.district)
            varname.thana = validated_data.get(validated_value).get('thana', varname.thana)
            varname.post_office = validated_data.get(validated_value).get('post_office', varname.post_office)
            varname.post_code = validated_data.get(validated_value).get('post_code', varname.post_code)
            varname.address_info = validated_data.get(validated_value).get('address_info', varname.address_info)
            output = varname.save()
            return output

        def parent_info_method(varname, validated_value):
            varname.parent_name = validated_data.get(validated_value).get('parent_name', varname.parent_name)
            varname.parent_date_of_birth = validated_data.get(validated_value).get('parent_date_of_birth',
                                                                                   varname.parent_date_of_birth)
            varname.parent_nid = validated_data.get(validated_value).get('parent_nid', varname.parent_nid)
            varname.occupation = validated_data.get(validated_value).get('occupation', varname.occupation)
            varname.organization_with_designation = validated_data.get(validated_value).get(
                'organization_with_designation', varname.organization_with_designation)
            varname.education = validated_data.get(validated_value).get('education', varname.education)
            varname.contact_number = validated_data.get(validated_value).get('contact_number', varname.contact_number)
            varname.parent_email = validated_data.get(validated_value).get('parent_email', varname.parent_email)
            output = varname.save()
            return output

        address_method(present_address, 'present_address')
        address_method(permanent_address, 'permanent_address')
        parent_info_method(father_info, 'father_info')
        parent_info_method(mother_info, 'mother_info')

        user.first_name = validated_data.get('user').get('first_name', user.first_name)
        user.last_name = validated_data.get('user').get('last_name', user.last_name)
        user.email = validated_data.get('user').get('email', user.email)
        user.save()

        # # get updated instance value
        instance.student_id = validated_data.get('student_id', instance.student_id)
        instance.student_roll_id = validated_data.get('student_roll_id', instance.student_roll_id)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.birth_certificate = validated_data.get('birth_certificate', instance.birth_certificate)
        instance.student_nid = validated_data.get('student_nid', instance.student_nid)
        instance.passport_number = validated_data.get('passport_number', instance.passport_number)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.religion = validated_data.get('religion', instance.religion)
        instance.guardian_name = validated_data.get('guardian_name', instance.guardian_name)
        instance.guardian_relation = validated_data.get('guardian_relation', instance.guardian_relation)
        instance.guardian_occupation = validated_data.get('guardian_occupation', instance.guardian_occupation)
        instance.yearly_income = validated_data.get('yearly_income', instance.yearly_income)
        instance.guardian_contact = validated_data.get('guardian_contact', instance.guardian_contact)
        instance.guardian_occupation = validated_data.get('guardian_occupation', instance.guardian_occupation)
        instance.guardian_email = validated_data.get('guardian_email', instance.guardian_email)
        instance.other_contact_person = validated_data.get('other_contact_person', instance.other_contact_person)
        instance.other_contact_person_relation = validated_data.get('other_contact_person_relation',
                                                                    instance.other_contact_person_relation)
        instance.other_contact_person_contact = validated_data.get('other_contact_person_contact',
                                                                   instance.other_contact_person_contact)
        instance.sibling_id = validated_data.get('sibling_id', instance.sibling_id)
        instance.previous_institution_name = validated_data.get('previous_institution_name',
                                                                instance.previous_institution_name)
        instance.previous_institution_contact = validated_data.get('previous_institution_contact',
                                                                   instance.previous_institution_contact)
        instance.previous_started_at = validated_data.get('previous_started_at', instance.previous_started_at)
        instance.previous_ending_at = validated_data.get('previous_ending_at', instance.previous_ending_at)
        instance.previous_ending_class = validated_data.get('previous_ending_class', instance.previous_ending_class)
        instance.previous_ending_result = validated_data.get('previous_ending_result', instance.previous_ending_result)
        instance.board_exam_name = validated_data.get('board_exam_name', instance.board_exam_name)
        instance.board_exam_registration = validated_data.get('board_exam_registration',
                                                              instance.board_exam_registration)
        instance.board_exam_roll = validated_data.get('board_exam_roll', instance.board_exam_roll)
        instance.board_exam_result = validated_data.get('board_exam_result', instance.board_exam_result)
        instance.admitted_department = validated_data.get('admitted_department', instance.admitted_department)
        instance.admitted_class = validated_data.get('admitted_class', instance.admitted_class)
        instance.admitted_group = validated_data.get('admitted_group', instance.admitted_group)
        instance.admitted_shift = validated_data.get('admitted_shift', instance.admitted_shift)
        instance.admitted_roll = validated_data.get('admitted_roll', instance.admitted_roll)
        instance.admitted_session = validated_data.get('admitted_session', instance.admitted_session)
        instance.student_blood_group = validated_data.get('student_blood_group', instance.student_blood_group)
        instance.special_body_sign = validated_data.get('special_body_sign', instance.special_body_sign)
        instance.academic_fees = validated_data.get('academic_fees', instance.academic_fees)
        instance.monthly_tution_fee = validated_data.get('monthly_tution_fee', instance.monthly_tution_fee)
        instance.boarding_feee = validated_data.get('boarding_feee', instance.boarding_feee)
        instance.admission_fee = validated_data.get('admission_fee', instance.admission_fee)
        instance.transport_fee = validated_data.get('transport_fee', instance.transport_fee)
        instance.tution_fee_active_from = validated_data.get('tution_fee_active_from', instance.tution_fee_active_from)
        instance.boarding_fee_active_from = validated_data.get('boarding_fee_active_from',
                                                               instance.boarding_fee_active_from)
        instance.transport_fee_active_from = validated_data.get('transport_fee_active_from',
                                                                instance.transport_fee_active_from)
        instance.is_tution_fee = validated_data.get('is_tution_fee', instance.is_tution_fee)
        instance.is_boarding_fee = validated_data.get('is_boarding_fee', instance.is_boarding_fee)
        instance.is_transport_fee = validated_data.get('is_transport_fee', instance.is_transport_fee)
        instance.talimi_murobbi_name = validated_data.get('talimi_murobbi_name', instance.talimi_murobbi_name)
        instance.eslahi_murobbi_name = validated_data.get('eslahi_murobbi_name', instance.eslahi_murobbi_name)
        instance.slug = validated_data.get('slug', instance.slug)

        instance.save()
        return instance


class OldStudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['admitted_department', 'admitted_class', 'admitted_group', 'admitted_shift', 'admitted_roll',
                  'admitted_session', 'monthly_tution_fee', 'boarding_feee',
                  'admission_fee', 'transport_fee', 'tution_fee_active_from', 'boarding_fee_active_from',
                  'transport_fee_active_from', 'is_tution_fee', 'is_boarding_fee', 'is_transport_fee',
                  'talimi_murobbi_name', 'eslahi_murobbi_name']

        def update(self, instance, validated_data):
            instance.admitted_department = validated_data.get('admitted_department', instance.admitted_department)
            instance.admitted_class = validated_data.get('admitted_class', instance.admitted_class)
            instance.admitted_group = validated_data.get('admitted_group', instance.admitted_group)
            instance.admitted_shift = validated_data.get('admitted_shift', instance.admitted_shift)
            instance.admitted_roll = validated_data.get('admitted_roll', instance.admitted_roll)
            instance.admitted_session = validated_data.get('admitted_session', instance.admitted_session)
            instance.monthly_tution_fee = validated_data.get('monthly_tution_fee', instance.monthly_tution_fee)
            instance.boarding_feee = validated_data.get('boarding_feee', instance.boarding_feee)
            instance.admission_fee = validated_data.get('admission_fee', instance.admission_fee)
            instance.transport_fee = validated_data.get('transport_fee', instance.transport_fee)
            instance.tution_fee_active_from = validated_data.get('tution_fee_active_from',
                                                                 instance.tution_fee_active_from)
            instance.boarding_fee_active_from = validated_data.get('boarding_fee_active_from',
                                                                   instance.boarding_fee_active_from)
            instance.transport_fee_active_from = validated_data.get('transport_fee_active_from',
                                                                    instance.transport_fee_active_from)
            instance.is_tution_fee = validated_data.get('is_tution_fee', instance.is_tution_fee)
            instance.is_boarding_fee = validated_data.get('is_boarding_fee', instance.is_boarding_fee)
            instance.is_transport_fee = validated_data.get('is_transport_fee', instance.is_transport_fee)
            instance.talimi_murobbi_name = validated_data.get('talimi_murobbi_name', instance.talimi_murobbi_name)
            instance.eslahi_murobbi_name = validated_data.get('eslahi_murobbi_name', instance.eslahi_murobbi_name)

            instance.save()
            return instance


class FessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FessInfo
        fields = '__all__'
