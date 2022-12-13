from django.contrib import admin
from library.models import LibraryBook, BookDistribution


# Register your models here.
@admin.register(LibraryBook)
class LibraryBookAdminView(admin.ModelAdmin):
    list_display = [
        'madrasha',
        'number',
        'name',
        'part',
        'category',
        'book_for_class',
        'translator',
        'publication',
        'original_writer',
        'language'
    ]


# Register your models here.
@admin.register(BookDistribution)
class BookDistributionAdminView(admin.ModelAdmin):
    list_display = [
        'madrasha',
        'student_roll_id',
        'book_number',
        'taken_date',
        'recipient_number',
    ]
