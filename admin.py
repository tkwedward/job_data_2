
from django.contrib import admin
from .models import User, Freelance
from .models import  labor_gov, collected_data
# Register your models here.

class labor_govAdmin(admin.ModelAdmin):
    model = labor_gov
    list_display = ('jobTitle', 'category', 'location2')
    search_fields = ('jobTitle', 'category', 'location2', 'company')

class collected_dataAdmin(admin.ModelAdmin):
    model = collected_data
    list_display = ('id','jobTitle', 'industry', 'salary_text','salary_type')
    list_editable = ('industry', 'salary_type')

admin.site.register(labor_gov, labor_govAdmin)
admin.site.register(Freelance)
admin.site.register(User)
admin.site.register(collected_data, collected_dataAdmin)
