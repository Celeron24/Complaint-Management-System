from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, default=None)

    def __str__(self):
        return self.name
