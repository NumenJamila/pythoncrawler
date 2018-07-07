from django.contrib import admin
from .models import ConferenceInfo

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('website', 'cnName', 'enName', 'introduce',
                    'location', 'sponsor', 'startdate', 'enddate',
                    'deadline', 'image', 'tag', 'pub_time', 'level',
                    'pub_time')
    list_filter = ('level',)

admin.site.register(ConferenceInfo,ArticleAdmin)
