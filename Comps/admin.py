from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from Comps.forms import CustomUserCreationForm
from .models import ComplaintType, Complaint


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


class DisplayToAdmin(admin.ModelAdmin):
    list_display = ['Comp_Assign', 'Subject', 'complaint_type', 'Description', 'created_at']
    list_filter = ['complaint_type']  # Add filters if needed
    search_fields = ['Subject', 'Description']  # Add search fields if needed


admin.site.register(Complaint, DisplayToAdmin)
# Unregister the default UserAdmin
admin.site.unregister(User)
# Register UserAdmin with the custom form
admin.site.register(User, CustomUserAdmin)
admin.site.register(ComplaintType)
