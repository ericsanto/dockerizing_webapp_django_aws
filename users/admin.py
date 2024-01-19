from django.contrib import admin
from .models import UserCustom


class UserCustomAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


admin.site.register(UserCustom, UserCustomAdmin)
