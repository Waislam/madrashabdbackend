"""
1. address serializer
2. madrasha serializer
3. User
4. MadrashaUserlisting
5. AvatarUpdateSerializer

"""
from django.contrib.auth.models import Group
from rest_framework import serializers
from accounts.models import (Division, District, Thana, PostOffice, PostCode, Address,
                             Madrasha, CustomUser, MadrashaUserListing)


# ======= 1. address serializer ================


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = [
            'pk',
            'name'
        ]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            'pk',
            'name',
            'division'
        ]


class ThanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thana
        fields = [
            'pk',
            'name',
            'district'
        ]


class PostOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = [
            'pk',
            'name',
            'district'
        ]


class PostCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCode
        fields = [
            'pk',
            'name',
            'post_office'
        ]


class AddressSerializer(serializers.ModelSerializer):
    # division = serializers.SerializerMethodField("division_name")
    # district = serializers.SerializerMethodField("district_name")
    # thana = serializers.SerializerMethodField("thana_name")
    # post_office = serializers.SerializerMethodField("post_office_name")
    # post_code = serializers.SerializerMethodField("post_code_name")

    # division = DivisionSerializer()
    # district = DistrictSerializer()
    # thana = ThanaSerializer()
    # post_office = PostOfficeSerializer()
    # post_code = PostCodeSerializer()

    class Meta:
        model = Address
        fields = ['id', 'division', 'district', 'thana', 'post_office', 'post_code', 'address_info']

    # def division_name(self, obj):
    #     name = obj.division.name
    #     return name


class AddressDetailSerializer(serializers.ModelSerializer):
    division = DivisionSerializer()
    district = DistrictSerializer()
    thana = ThanaSerializer()
    post_office = PostOfficeSerializer()
    post_code = PostCodeSerializer()

    class Meta:
        model = Address
        fields = ['id', 'division', 'district', 'thana', 'post_office', 'post_code', 'address_info']


# ============ 2. madrasha serializer =============


class MadrashaSerializer(serializers.ModelSerializer):
    madrasha_address = AddressSerializer()

    class Meta:
        model = Madrasha
        fields = ['id', 'name', 'madrasha_code', 'madrasha_address', 'madrasha_logo', 'created_by', 'updated_by',
                  'active_status', 'slug']

    def create(self, validated_data):
        address_data = validated_data['madrasha_address']
        madrasha_name = validated_data['name']
        created_by = validated_data['created_by']
        updated_by = validated_data['updated_by']

        address = Address.objects.create(**address_data)

        madrasha = Madrasha.objects.create(madrasha_address=address,
                                           name=madrasha_name,
                                           created_by=created_by,
                                           updated_by=updated_by)
        return madrasha

    def update(self, instance, validated_data):
        """
        1. get the current instance name
        2. get the nested and save the obj
        3. get other fields of instance and save it
        """
        instance.name = validated_data.get('name')

        # Get madrasha instance
        madrasha_address = instance.madrasha_address

        # Save madrasha address
        madrasha_address.division = validated_data.get('madrasha_address').get('division',
                                                                               instance.madrasha_address.division)
        madrasha_address.district = validated_data.get('madrasha_address').get('district',
                                                                               instance.madrasha_address.district)
        madrasha_address.post_office = validated_data.get('madrasha_address').get('post_office',
                                                                                  instance.madrasha_address.post_office)
        madrasha_address.post_code = validated_data.get('madrasha_address').get('post_code',
                                                                                instance.madrasha_address.post_code)
        madrasha_address.thana = validated_data.get('madrasha_address').get('thana', instance.madrasha_address.thana)
        madrasha_address.address_info = validated_data.get('madrasha_address').get('address_info',
                                                                                   instance.madrasha_address.address_info)
        madrasha_address.save()
        # get other fields of instance and save it
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.updated_by = validated_data.get('updated_by', instance.updated_by)
        instance.active_status = validated_data.get('active_status', instance.active_status)
        instance.save()
        return instance


class MadrashaLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Madrasha
        fields = "__all__"


# ================== 3. User ============
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    madrasha_id = serializers.CharField(style={"input_type": "text"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'password', 'password2', "madrasha_id"]
        extra_kwargs = {
            'password': {'write_only': True},
            'madrasha_id': {'write_only': True}
        }

    def save(self, **kwargs):
        phone = self.validated_data['phone']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        madrasha_id = self.validated_data['madrasha_id']

        user = CustomUser(phone=phone, username=phone)
        if password != password2:
            raise serializers.ValidationError({'message': 'password must match'})
        user.set_password(password)
        user.save()
        MadrashaUserListing.objects.create(user=user, madrasha_id=madrasha_id)

        return user


# ================== 4. MadrashaUserlisting  ============

class MadrashaUserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MadrashaUserListing
        fields = ['user', 'madrasha']


# =================== 5. AvatarUpdateSerializer =================
class AvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar']

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.pk = validated_data.get('user_id', instance.pk)
        instance.save()
        return instance


# ============ 2. customuser serializer =============
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # exclude = ["password", 'avatar']
        exclude = ['avatar']


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", 'last_name', 'email']


class CustomUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class CustomUserLoginSerializer(serializers.ModelSerializer):
    groups = GroupsSerializer(many=True)

    class Meta:
        model = CustomUser
        exclude = ['password']
