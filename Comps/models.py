from django.db import models


class Complaint(models.Model):
    COMP_ASSIGN_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Assignment', 'Assignment'),
    ]

    Comp_Assign = models.CharField(max_length=50)
    Subject = models.CharField(max_length=200)
    complaint_type = models.CharField(max_length=50)
    Description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Ip address and computer name, username some changes 

    def __str__(self):
        return self.Subject
