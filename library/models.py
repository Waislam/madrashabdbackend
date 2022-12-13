import datetime
from datetime import date
from django.db import models
from accounts.models import Madrasha
from students.models import Student
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
BOOK_CATEGORY = (('nesabi', 'Nesabi'),
                 ('hadis/usolehadis', 'Hadis/Usolehadis'),
                 ('fekah/usolefekhan', 'Fekah/Usolefekhan'),
                 ('tafsir', 'Tafsir'),
                 ('mantek', 'Mantek'),
                 ('quran', 'Quran'),
                 ('akida', 'Akida'),
                 ('etihash', 'Etihash'),
                 ('orthoniti', 'Orthoniti'),
                 ('vugol', 'Vugol'),
                 ('arbi shahitto', 'Arbi shahitto'),
                 ('nahu', 'Nahu'),
                 ('sorof', 'Sorof'),
                 ('sirat', 'Sirat'),
                 ('eslah', 'Eslah'),
                 ('ovidhan', 'Ovidhan'),
                 ('golpo shahitto', 'Golpo shahitto'),
                 ('fatwa', 'Fatwa'),
                 ('ralagad', 'Balagad'),
                 ('rasayel', 'Rasayel'),
                 ('other', 'Other'),
                 )


class LibraryBook(models.Model):
    madrasha = models.ForeignKey(
        Madrasha, on_delete=models.CASCADE,
        related_name='library_books',
        null=True,
        blank=True)
    number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    part = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, choices=BOOK_CATEGORY, default='Nesabi')
    book_for_class = models.CharField(max_length=100, blank=True, null=True)
    translator = models.CharField(max_length=100, blank=True, null=True)
    publication = models.CharField(max_length=100, blank=True, null=True)
    original_writer = models.CharField(max_length=200, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(default=date.today)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BookDistribution(models.Model):
    madrasha = models.ForeignKey(
        Madrasha,
        on_delete=models.CASCADE,
        related_name='book_distribution',
        null=True, blank=True)
    student_roll_id = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='student',
        null=True, blank=True)
    book_number = models.ForeignKey(
        LibraryBook,
        on_delete=models.CASCADE,
        related_name='library_book',
        null=True, blank=True)
    taken_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='user_book_distribution', null=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name='user', null=True
    )
    recipient_number = models.CharField(max_length=120, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     recipient = BookDistribution.objects.filter(
    #         created_at__year=datetime.datetime.now().year,
    #         created_at__month=datetime.datetime.now().month,
    #         created_at__day=datetime.datetime.now().day
    #     )
    #
    #     recipient_number = "Book-" + datetime.datetime.today().strftime("%d-%m-%y") + '-' + str(int(recipient) + 1)
    #     if not self.recipient_number:
    #         self.recipient_number = recipient_number
    #     super(BookDistribution, self).save(*args, **kwargs)
    #
    # def __str__(self):
    #     return self.recipient_number

    class Meta:
        ordering = ['-created_at']
