from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import ComplaintType, Complaint, Employee


admin.site.register(Employee)
admin.site.register(Complaint)
# admin.site.unregister(User)
admin.site.register(ComplaintType)
# admin.site.unregister(Group)
