from django.db import models
from accounts.models import Madrasha


# Create your models here.
class Committee(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, blank=True, null=True)
    member_name = models.CharField(max_length=255, blank=True, null=True)
    member_designation = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        unique_together = [['phone_number', 'madrasha']]
        ordering = ['member_name']

    def __str__(self):
        return self.member_name


class PermanentMembers(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, blank=True, null=True)
    member_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    monthly_contribution = models.IntegerField(blank=True, null=True)
    yearly_contribution = models.IntegerField(blank=True, null=True)
    is_monthly_contribution = models.BooleanField(default=False)
    is_yearly_contribution = models.BooleanField(default=False)

    class Meta:
        unique_together = [['phone_number', 'madrasha']]
        ordering = ['member_name']

    def __str__(self):
        return str(self.id)


class OtherMembers(models.Model):
    madrasha = models.ForeignKey(Madrasha, on_delete=models.CASCADE, blank=True, null=True)
    member_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        unique_together = [['phone_number', 'madrasha']]
        ordering = ['member_name']

    def __str__(self):
        return str(self.id)