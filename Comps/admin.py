from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from Comps.forms import CustomUserCreationForm
from .models import ComplaintType, Complaint, Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_name']

    def has_add_permission(self, request):
        # Allow adding only if the user is an admin
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Allow changing only if the user is an admin
        return request.user.is_superuser


admin.site.register(Employee, EmployeeAdmin)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


class DisplayToAdmin(admin.ModelAdmin):
    list_display = ['user', 'Comp_Assign', 'Subject', 'complaint_type', 'Description', 'created_at']
    list_filter = ['user', 'complaint_type']  # Add filters if needed
    search_fields = ['user__username', 'Subject', 'Description']  # Add 'user__username' for searching by username

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # Existing object, make user field read-only
            readonly_fields += ('user',)
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:  # Existing object, add 'user' fieldset at the top
            user_fieldset = ('User Information', {'fields': ()})
            fieldsets = (user_fieldset,) + tuple(fieldsets)  # Convert fieldsets to tuple before concatenating
        return fieldsets


admin.site.register(Complaint, DisplayToAdmin)
# Unregister the default UserAdmin
admin.site.unregister(User)
# Register UserAdmin with the custom form
admin.site.register(User, CustomUserAdmin)
admin.site.register(ComplaintType)
admin.site.unregister(Group)
