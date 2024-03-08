from django.db import models
from django.contrib.auth.models import User


class ComplaintType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    # employee = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    emp_name = models.CharField(max_length=30, unique=True, default=None)

    def __str__(self):
        return f'{self.emp_name}'


class Complaint(models.Model):
    COMP_ASSIGN_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Assignment', 'Assignment'),
    ]

    status_choices = [
        (1, 'InProgress'),
        (2, 'Solved')
    ]
    status = models.IntegerField(choices=status_choices, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Comp_Assign = models.CharField(max_length=50, choices=COMP_ASSIGN_CHOICES, default='Complaint')
    Subject = models.CharField(max_length=50)
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE, null=True)
    Description = models.TextField(null=True, blank=True, verbose_name='Explain in more detail')
    created_at = models.DateTimeField(auto_now_add=True)

    assigned_employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.Comp_Assign} - {self.Subject} - {self.created_at}'


class Comment(models.Model):
    post = models.ForeignKey(Complaint, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.user, self.name)
