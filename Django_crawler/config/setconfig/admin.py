from django.contrib import admin
from .models import Config

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('website_select', 'website_reg','cnName_select', 'cnName_reg', 'enName_select',
                    'enName_reg', 'introduce_select', 'introduce_reg', 'location_select',
                    'location_reg', 'sponsor_select', 'sponsor_reg', 'startdate_select',
                    'startdate_reg', 'enddate_select', 'enddate_reg', 'deadline_select',
                    'deadline_reg', 'image_select', 'image_reg', 'tag_select', 'tag_reg',
                    'req_url','taskname')

admin.site.register(Config,ArticleAdmin)
