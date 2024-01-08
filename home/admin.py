from django.contrib import admin
from .models import *


class SchedulingAdmin(admin.ModelAdmin):
    list_display = ['user', 'day', 'time', 'service',]


class BarbersTeamAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Services)
admin.site.register(Scheduling, SchedulingAdmin)
admin.site.register(BarbersTeam, BarbersTeamAdmin)
