from django.db import models

# Create your models here.
class Process(models.Model):
    process_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.process_name