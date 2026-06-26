from django.db import models

# Create your models here.
class Conferencename(models.Model):
    name = models.CharField(max_length=200, unique=True)
    normalregistration_fee = models.CharField(max_length=200)
    lateregistration_fee = models.CharField(max_length=200)
    lateregistration_start_date = models.DateField(null=True, blank=True)
    conferencestartdate = models.DateField(null=True, blank=True)
    conferenceenddate = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    venue = models.CharField(max_length=300, blank=True, null=True)



    def __str__(self):
        return self.name