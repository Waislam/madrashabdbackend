from django.db import models
from accounts.models import Address, Madrasha
from students.models import Student

MEASUREMENT_CHOICE = (
    ('kg', 'Kg'),
    ('litre', 'Litre'),
    ('gm', 'Gm'),
)


# class BazarList(models.Model):
#     madrasha = models.ForeignKey(Madrasha, on_delete=models.SET_NULL, related_name='bazarList_madrasha', null=True)
#     date = models.DateField(blank=True, null=True)
#     total_cost = models.CharField(max_length=250, blank=True, null=True)

    # def __str__(self):
    #     return str(self.date)


# class BazarItem(models.Model):
#     madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name='bazarItem_madrasha')
#     bazar_list = models.ForeignKey(BazarList, on_delete=models.CASCADE, related_name='bazarlist_items', blank=True, null=True)
#     bazar_item_name = models.CharField(max_length=250)
#     quantity = models.CharField(max_length=250)
#     measurement = models.CharField(max_length=10, choices=MEASUREMENT_CHOICE, default='Kg')
#     amount = models.CharField(max_length=250)
#     consumption = models.CharField(max_length=250)
#     total_stock = models.CharField(max_length=250, blank=True, null=True)


class DailyBazar(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name='bazarItem_madrasha')
    bazar_item_name = models.CharField(max_length=250)
    quantity = models.CharField(max_length=250)
    measurement = models.CharField(max_length=10, choices=MEASUREMENT_CHOICE, default='Kg')
    amount = models.CharField(max_length=250)
    consumption = models.CharField(max_length=250)
    total_stock = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return self.bazar_item_name


class KhabarDistribution(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, related_name='khabar_distribution_madrasha')
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='khabar_distribution_student')
    date = models.DateField(null=True, blank=True)
    is_breakfast = models.BooleanField(default=False)
    is_lunch = models.BooleanField(default=False)
    is_dinner = models.BooleanField(default=False)

    def __str__(self):
        return self.student.student_id
