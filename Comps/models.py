from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ComplaintType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    emp_name = models.CharField(max_length=30, unique=True, default=None)

    def __str__(self):
        return f'{self.emp_name}'


class Complaint(models.Model):
    COMP_ASSIGN_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Assignment', 'Assignment'),
    ]

    status_choices = [
        (3, 'Pending'),
        (2, 'InProgress'),
        (1, 'Solved'),
    ]
    status = models.IntegerField(choices=status_choices, default=3)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Comp_Assign = models.CharField(max_length=50, choices=COMP_ASSIGN_CHOICES, default='Complaint')
    Subject = models.CharField(max_length=50)
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, null=True)
    Description = models.TextField(null=True, blank=True, verbose_name='Explain in more detail')
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    assigned_employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Comp_Assign} - {self.Subject} - {self.created_at}'


class Comment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_admin_comment = models.BooleanField(default=True)  # Add this field to mark adminsite comments
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}-{}'.format(self.complaint.Subject, str(self.user.username))
