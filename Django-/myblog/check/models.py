from django.db import models


# Create your models here.
class ConferenceInfo(models.Model):
    website = models.CharField(max_length=500, default='null')
    cnName = models.CharField(max_length=500, default='null')
    enName = models.CharField(max_length=500, default='null')
    introduce = models.CharField(max_length=3000, default='null')
    location = models.CharField(max_length=500, default='null')
    sponsor = models.CharField(max_length=500, default='null')
    startdate = models.DateField(null=True)
    enddate = models.DateField(null=True)
    deadline = models.DateField(null=True)
    image = models.CharField(max_length=500, default='null')
    tag = models.CharField(max_length=500, default='null')
    pub_time = models.DateField(null=True)
    TAG_CHOICES = (
        ('普通','普通'),
        ('紧急','紧急'),
    )
    level = models.CharField(null=True, blank=True, max_length=5, choices=TAG_CHOICES)

    def __str__(self):
        return self.website
