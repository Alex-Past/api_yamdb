from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio'
    )
    list_editable = ('role',)
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = 'Не задано'


admin.site.register(User, UserAdmin)
