from rest_framework import serializers
from .models import (
    Committee,
    PermanentMembers,
    OtherMembers
)


class CommitteeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = [
            'id',
            'madrasha',
            'member_name',
            'member_designation',
            'phone_number'
        ]

        depth = 2


class CommitteeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = [
            'id',
            'madrasha',
            'member_name',
            'member_designation',
            'phone_number'
        ]


class PermanentMembersListSerializers(serializers.ModelSerializer):
    class Meta:
        model = PermanentMembers
        fields = [
            'id',
            'madrasha',
            'member_name',
            'address',
            'phone_number'
        ]

        depth = 2


class PermanentMembersSerializers(serializers.ModelSerializer):
    class Meta:
        model = PermanentMembers
        fields = [
            'id',
            'madrasha',
            'member_name',
            'address',
            'phone_number'
        ]


class OthersMemberListSerializers(serializers.ModelSerializer):
    class Meta:
        model = OtherMembers
        fields = [
            'id',
            'madrasha',
            'member_name',
            'address',
            'phone_number'
        ]

        depth = 2


class OthersMemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = OtherMembers
        fields = [
            'id',
            'madrasha',
            'member_name',
            'address',
            'phone_number'
        ]
