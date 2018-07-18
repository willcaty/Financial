from django.db import models
from datetime import date


# Create your models here.


class QIMAN(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    PE_PB = models.FloatField()
    percentile = models.FloatField(blank=True)
    high = models.FloatField()
    low = models.FloatField()
    roe = models.FloatField()
    color = models.TextField(max_length=20)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.name




