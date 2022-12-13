from rest_framework import serializers
from library.models import LibraryBook, BookDistribution


class LibraryBookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ['id', 'madrasha', 'number', 'name', 'part', 'category', 'book_for_class',
                  'translator', 'publication', 'original_writer', 'language', 'is_available']
        depth = 3  # if you use depth you no need to use nested serializer to show dictionary of nested obj

    def __init__(self, *args, **kwargs):
        super(LibraryBookCreateSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class LibraryBookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = ['id', 'madrasha', 'name', 'part', 'category', 'book_for_class',
                  'translator', 'publication', 'original_writer', 'language', 'is_available']


class BookDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDistribution
        fields = [
            'id',
            'madrasha',
            'student_roll_id',
            'book_number',
            'taken_date',
            'recipient_number',

        ]
        depth = 2

    def __init__(self, *args, **kwargs):
        super(BookDistributionSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2


class BookDistributionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDistribution
        fields = [
            'id',
            'madrasha',
            'student_roll_id',
            'book_number',
            'taken_date',
            'recipient_number',
        ]