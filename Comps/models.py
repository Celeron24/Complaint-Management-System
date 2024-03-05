from django.db import models


class ComplaintType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Complaint(models.Model):
    COMP_ASSIGN_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Assignment', 'Assignment'),
    ]

    user_name = models.CharField(max_length=20, default='Anonymous')
    Comp_Assign = models.CharField(max_length=50, choices=COMP_ASSIGN_CHOICES, default=None)
    Subject = models.CharField(max_length=50)
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.CASCADE)
    Description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Ip address and computer name, username some changes 

    def __str__(self):
        return f'{self.user_name} - {self.created_at} - {self.Subject}'
