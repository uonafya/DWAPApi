from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
admin.site.register(RoleScreens)

@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_superuser', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'organisation', 'phone')}),
        ('Permissions', {'fields': ('user_permissions',
         'groups', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'username', 'email', 'first_name', 'last_name', 'organisation', 'phone', 'groups', 'user_permissions', 'is_active', 'is_staff', 'is_superuser')}
         ),
    )
