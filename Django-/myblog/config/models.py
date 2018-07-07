from django.db import models


# Create your models here.
class Article(models.Model):
    req_url = models.CharField(max_length=500, default='null')
    website_select = models.CharField(max_length=500, default='null')
    website_reg = models.CharField(max_length=500, default='null')
    cnName_select = models.CharField(max_length=500, default='null')
    cnName_reg = models.CharField(max_length=500, default='null')
    enName_select = models.CharField(max_length=500, default='null')
    enName_reg = models.CharField(max_length=500, default='null')
    introduce_select = models.CharField(max_length=3000, default='null')
    introduce_reg = models.CharField(max_length=3000, default='null')
    location_select = models.CharField(max_length=500, default='null')
    location_reg = models.CharField(max_length=500, default='null')
    sponsor_select = models.CharField(max_length=500, default='null')
    sponsor_reg = models.CharField(max_length=500, default='null')
    startdate_select = models.CharField(max_length=500, default='null')
    startdate_reg = models.CharField(max_length=500, default='null')
    enddate_select = models.CharField(max_length=500, default='null')
    enddate_reg = models.CharField(max_length=500, default='null')
    deadline_select = models.CharField(max_length=500, default='null')
    deadline_reg = models.CharField(max_length=500, default='null')
    image_select = models.CharField(max_length=500, default='null')
    image_reg = models.CharField(max_length=500, default='null')
    tag_select = models.CharField(max_length=500, default='null')
    tag_reg = models.CharField(max_length=500, default='null')
    pub_time = models.DateField(null=True)
    TAG_CHOICES = (
        ('普通', '普通'),
        ('紧急', '紧急'),
    )
    level = models.CharField(null=True, blank=True, max_length=5, choices=TAG_CHOICES)

    def __str__(self):
        return self.website_select
