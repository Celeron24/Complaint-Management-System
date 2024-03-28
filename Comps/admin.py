from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from Comps.forms import CustomUserCreationForm
from .models import ComplaintType, Complaint, Employee, Comment


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'Description', 'created_at']
    search_fields = ['user__username', 'description']  # Enable searching by user's name
    list_filter = ['user']  # Add filter by user's name

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:  # Limit complaints to the current user if not superuser
            queryset = queryset.filter(user=request.user)
        return queryset


admin.site.register(Complaint, ComplaintAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['emp_name']

    def has_add_permission(self, request):
        # Allow adding only if the user is an adminsite
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Allow changing only if the user is an adminsite
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


# Unregister the default UserAdmin
admin.site.unregister(User)
# Register UserAdmin with the custom form
admin.site.register(User, CustomUserAdmin)
admin.site.register(ComplaintType)
admin.site.unregister(Group)
admin.site.register(Comment)
