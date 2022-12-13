from rest_framework import serializers
# from .models import BazarList, BazarItem
from accounts.serializers import MadrashaSerializer
from boarding.models import DailyBazar


# class BazarItemSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = BazarItem
#         fields = '__all__'


# class BazarListSerializer(serializers.ModelSerializer):
#     item = BazarItemSerializer()
#
#     class Meta:
#         model = BazarList
#         fields = [
#             'id',
#             'madrasha',
#             'date',
#             'total_cost',
#             'item'
#         ]
#
#     def create(self, validated_data):
#         validated_date = validated_data.pop('date')
#         item = validated_data.pop('item')
#         # item_obj = BazarItem.objects.create(**item)
#
#         ## get last object date
#         # last_obj = BazarList.objects.all().last()
#         # if last_obj.date == validated_date:
#         bazar_list = BazarList.objects.get_or_create(date=validated_date, **validated_data)
#         item_obj = BazarItem.objects.create(**item)
#
#         print("bazar_list: ", bazar_list)
#         # addd bazar list as foreignkey to item obj
#         item_obj.bazar_list = bazar_list
#         # item_obj.save()
#         # return bazar_list
#         return "something"

class DailyBazarSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyBazar
        fields = '__all__'


class DailyBazarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyBazar
        fields = '__all__'
        depth = 2


