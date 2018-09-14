from django.contrib import admin
from .models import Conference

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('website', 'cnName', 'enName', 'introduce',
                    'location', 'sponsor', 'startdate', 'enddate',
                    'deadline', 'image', 'tag')

admin.site.register(Conference,ArticleAdmin)
