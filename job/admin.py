from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . models import JobListing
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','location','company','created_at','is_filled']

admin.site.register(JobListing,PostAdmin)

