from django.contrib import admin
from adminsite.models import Department, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    # Remove fields from the add and change forms
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'name', 'designation'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'name', 'designation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_display = ('username', 'name', 'designation', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'name', 'designation')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.unregister(User)
