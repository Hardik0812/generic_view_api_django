from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


class Students(models.Model):
    name = models.CharField(max_length = 100)
    address = models.TextField()
    gender = models.CharField( max_length=50)
    rollnumber = models.IntegerField()


    def __str__(self):
        return self.name + " " + self.rollnumber
