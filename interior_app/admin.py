from django.contrib import admin
from .models import *


class CategoriesAdmin(admin.ModelAdmin):

	prepopulated_fields = {"slug": ("name",)}

# Register your models here.

admin.site.register(LocationData)
admin.site.register(Locations)
admin.site.register(Categories,CategoriesAdmin)
admin.site.register(ScrapLocations)
admin.site.register(ScrapeStatus)
