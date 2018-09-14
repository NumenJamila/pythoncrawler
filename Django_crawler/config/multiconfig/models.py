from django.db import models

# Create your models here.
class Multiconf(models.Model):
    taskname = models.CharField(max_length=500, default='null')
    confConfigFileNames = models.CharField(max_length=500, default='null')
    txtConfigFileNames = models.CharField(max_length=500, default='null')
    

    def __str__(self):
        return self.taskname