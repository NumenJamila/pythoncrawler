from django.contrib import admin
from .models import Multiconf

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('taskname', 'confConfigFileNames', 'txtConfigFileNames')

admin.site.register(Multiconf,ArticleAdmin)
