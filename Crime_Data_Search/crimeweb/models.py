from django.db import models

class MyData(models.Model):
    arrested = models.BooleanField()
    city = models.CharField(max_length=100)
    crime_types = models.CharField(max_length=100)
    perpetrator_age = models.IntegerField()
    perpetrator_sex = models.CharField(max_length=10)
    victim_age = models.IntegerField()
    victim_sex = models.CharField(max_length=10)
    date = models.DateField()