#admin.py
from tracking.models import *
from django.contrib import admin
'''
class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1

class WOInline(admin.TabularInline):
    model = WorkOrder
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fields = ['Number',  'Name', 'Contractor', 'Installer', 'City', 'State']
    inlines = [ProjectInline]

class VehicleModelAdmin(admin.ModelAdmin):
    fields = ['carManufacturer','model']
    #inlines = [codeInline]
'''
admin.site.register(WorkOrder)
admin.site.register(Engineer)
admin.site.register(Installer)
admin.site.register(Project)
admin.site.register(Contractor)
admin.site.register(Driver)
#admin.site.register(ProjectAdmin)
#admin.site.register(WOInline)