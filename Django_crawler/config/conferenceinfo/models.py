from django.db import models


# Create your models here.
class Conference(models.Model):
    taskname = models.CharField(max_length=500, default='null')
    website = models.CharField(max_length=500, default='null')
    cnName = models.CharField(max_length=500, default='null')
    enName = models.CharField(max_length=500, default='null')
    introduce = models.CharField(max_length=3000, default='null')
    location = models.CharField(max_length=500, default='null')
    sponsor = models.CharField(max_length=500, default='null')
    startdate = models.DateTimeField(null=True, blank=True)
    enddate = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    image = models.CharField(max_length=500, default='null')
    tag = models.CharField(max_length=500, default='null')

    def __str__(self):
        return self.website
