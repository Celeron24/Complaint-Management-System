from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from Comps.forms import CustomUserCreationForm
from .models import ComplaintType, Complaint


admin.site.unregister(Group)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


class DisplayToAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'Comp_Assign', 'Subject', 'complaint_type', 'Description', 'created_at']
    list_filter = ['user_name', 'complaint_type']  # Add filters if needed
    search_fields = ['user_name', 'Subject', 'Description']  # Add search fields if needed


admin.site.register(Complaint, DisplayToAdmin)
# Unregister the default UserAdmin
admin.site.unregister(User)
# Register UserAdmin with the custom form
admin.site.register(User, CustomUserAdmin)
admin.site.register(ComplaintType)
