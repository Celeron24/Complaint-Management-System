from django.contrib import admin
from adminsite.models import Department, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'designation', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'name', 'designation' , 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_display = ('username', 'name', 'designation', 'department', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'name', 'designation', 'department')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
# admin.site.unregister(User)

