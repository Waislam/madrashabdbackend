from rest_framework import serializers

from accounts.serializers import (
    CustomUserSerializer,
    MadrashaSerializer,
    AddressDetailSerializer,
    CustomUserListSerializer, CustomUserUpdateSerializer
)
from .models import (
    Teacher,
    Education,
    Skill,
    Experience
)
from students.serializers import AddressSerializer
from accounts.models import Address, CustomUser
from settingapp.serializers import DepartmentSerializer, DesignationSerializer


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'degree_name', 'institution_name', 'passing_year', 'result']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'experience_name']


class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    present_address = AddressSerializer()
    permanent_address = AddressSerializer()
    education = EducationSerializer()
    skill = SkillSerializer()
    experience = ExperienceSerializer()

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'madrasha', 'teacher_id', 'father_name', 'mother_name', 'date_of_birth', 'gender',
            'religion', 'marital_status', 'present_address', 'permanent_address', 'education', 'skill',
            'phone_home', 'nid', 'birth_certificate', 'nationality', 'blood_group', "experience", 'department',
            'designation', 'starting_date', 'ending_date', 'slug'
        ]

    def create(self, validated_data):
        user_object = validated_data.pop('user')
        present_address = validated_data.pop('present_address')
        permanent_address = validated_data.pop('permanent_address')
        education = validated_data.pop('education')
        skill = validated_data.pop('skill')
        experience = validated_data.pop('experience')

        present_address_obj = Address.objects.create(**present_address)
        permanent_address_obj = Address.objects.create(**permanent_address)

        education_obj = Education.objects.create(**education)
        skill_obj = Skill.objects.create(**skill)
        experience_obj = Experience.objects.create(**experience)

        ##create user
        user_created = CustomUser.objects.create(**user_object)

        # now create teacher obj
        teacher = Teacher.objects.create(
            user=user_created,
            present_address=present_address_obj,
            permanent_address=permanent_address_obj,
            education=education_obj,
            experience=experience_obj,
            skill=skill_obj,
            **validated_data
        )
        return teacher

    # def update(self, instance, validated_data):
    #     # get all nested obj
    #
    #     present_address = instance.present_address
    #     permanent_address = instance.permanent_address
    #     education = instance.education
    #     skill = instance.skill
    #
    #     # get updated fields value for every nested obj
    #     def address_method(varname, validated_value):
    #         varname.division = validated_data.get(validated_value).get('division', varname.division)
    #         varname.district = validated_data.get(validated_value).get('district', varname.district)
    #         varname.thana = validated_data.get(validated_value).get('thana', varname.thana)
    #         varname.post_office = validated_data.get(validated_value).get('post_office', varname.post_office)
    #         varname.post_code = validated_data.get(validated_value).get('post_code', varname.post_code)
    #         varname.address_info = validated_data.get(validated_value).get('address_info', varname.address_info)
    #         output = varname.save()
    #         return output
    #
    #     address_method(present_address, 'present_address')
    #     address_method(permanent_address, 'permanent_address')
    #
    #     education.degree_name = validated_data.get('education').get('degree_name', education.degree_name)
    #     education.institution_name = validated_data.get('education').get('institution_name', education.institution_name)
    #     education.passing_year = validated_data.get('education').get('passing_year', education.passing_year)
    #     education.result = validated_data.get('education').get('result', education.result)
    #     education.save()
    #
    #     skill.skill_name = validated_data.get('skill').get('skill_name', skill.skill_name)
    #     skill.save()
    #
    #     # get instance fields
    #     instance.father_name = validated_data.get('father_name', instance.father_name)
    #     instance.mother_name = validated_data.get('mother_name', instance.mother_name)
    #     instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
    #     instance.religion = validated_data.get('religion', instance.religion)
    #     instance.marital_status = validated_data.get('marital_status', instance.marital_status)
    #     instance.phone_home = validated_data.get('phone_home', instance.phone_home)
    #     instance.nid = validated_data.get('nid', instance.nid)
    #     instance.birth_certificate = validated_data.get('birth_certificate', instance.birth_certificate)
    #     instance.nationality = validated_data.get('nationality', instance.nationality)
    #     instance.blood_group = validated_data.get('blood_group', instance.blood_group)
    #     instance.department = validated_data.get('department', instance.department)
    #     instance.designation = validated_data.get('designation', instance.designation)
    #     instance.starting_date = validated_data.get('starting_date', instance.starting_date)
    #     instance.ending_date = validated_data.get('ending_date', instance.ending_date)
    #     instance.slug = validated_data.get('slug', instance.slug)
    #
    #     instance.save()
    #     return instance


class TeacherUpdateSerializer(serializers.ModelSerializer):
    user = CustomUserUpdateSerializer()
    present_address = AddressSerializer()
    permanent_address = AddressSerializer()
    education = EducationSerializer()
    skill = SkillSerializer()
    experience = ExperienceSerializer()

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'madrasha', 'teacher_id', 'father_name', 'mother_name', 'date_of_birth', 'gender',
            'religion', 'marital_status', 'present_address', 'permanent_address', 'education', 'skill', 'experience',
            'phone_home', 'nid', 'birth_certificate', 'nationality', 'blood_group', 'department',
            'designation', 'starting_date', 'ending_date', 'slug'
        ]

    def update(self, instance, validated_data):
        # get all nested obj
        user = instance.user
        present_address = instance.present_address
        permanent_address = instance.permanent_address
        education = instance.education
        skill = instance.skill
        experience = instance.experience

        # print("skil intance before update: ", skill)

        # get updated fields value for every nested obj
        def address_method(varname, validated_value):
            varname.division = validated_data.get(validated_value).get('division', varname.division)
            varname.district = validated_data.get(validated_value).get('district', varname.district)
            varname.thana = validated_data.get(validated_value).get('thana', varname.thana)
            varname.post_office = validated_data.get(validated_value).get('post_office', varname.post_office)
            varname.post_code = validated_data.get(validated_value).get('post_code', varname.post_code)
            varname.address_info = validated_data.get(validated_value).get('address_info', varname.address_info)
            output = varname.save()
            return output

        address_method(present_address, 'present_address')
        address_method(permanent_address, 'permanent_address')

        education.degree_name = validated_data.get('education').get('degree_name', education.degree_name)
        education.institution_name = validated_data.get('education').get('institution_name', education.institution_name)
        education.passing_year = validated_data.get('education').get('passing_year', education.passing_year)
        education.result = validated_data.get('education').get('result', education.result)
        education.save()

        user.first_name = validated_data.get('user').get('first_name', user.first_name)
        user.last_name = validated_data.get('user').get('last_name', user.last_name)
        user.email = validated_data.get('user').get('email', user.email)
        user.save()
        # try:
        skill.skill_name = validated_data.get('skill').get('skill_name', skill.skill_name)
        skill.save()

        experience.experience_name = validated_data.get('experience').get('experience_name', experience.experience_name)
        experience.save()


        ## add nested updated field
        # instance.skill = validated_data.get('skill', skill)
        # get instance fields
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.mother_name = validated_data.get('mother_name', instance.mother_name)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.religion = validated_data.get('religion', instance.religion)
        instance.marital_status = validated_data.get('marital_status', instance.marital_status)
        instance.phone_home = validated_data.get('phone_home', instance.phone_home)
        instance.nid = validated_data.get('nid', instance.nid)
        instance.birth_certificate = validated_data.get('birth_certificate', instance.birth_certificate)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.blood_group = validated_data.get('blood_group', instance.blood_group)
        instance.department = validated_data.get('department', instance.department)
        instance.designation = validated_data.get('designation', instance.designation)
        instance.starting_date = validated_data.get('starting_date', instance.starting_date)
        instance.ending_date = validated_data.get('ending_date', instance.ending_date)
        instance.slug = validated_data.get('slug', instance.slug)

        instance.save()
        return instance


class TeacherListSerializer(serializers.ModelSerializer):
    user = CustomUserListSerializer()
    madrasha = MadrashaSerializer()
    present_address = AddressDetailSerializer()
    permanent_address = AddressDetailSerializer()
    education = EducationSerializer()
    skill = SkillSerializer()
    department = DepartmentSerializer()
    designation = DesignationSerializer()
    experience = ExperienceSerializer()

    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'madrasha', 'teacher_id', 'father_name', 'mother_name', 'date_of_birth', 'gender', 'religion',
            'marital_status', 'present_address', 'permanent_address', 'education', 'skill',
            'phone_home', 'nid', 'birth_certificate', 'nationality', 'blood_group', 'department',
            'designation', 'starting_date', 'ending_date', 'slug', 'experience'
        ]
