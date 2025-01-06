from django.db import models

# Create your models here.
class Process(models.Model):
    name = models.CharField(max_length=100, unique=True)  # English name, must be unique
    name_mal = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)  # Description in English
    description_mal = models.TextField(blank=True, null=True) 
    def __str__(self):
        return self.name