from django.db import models

# Create your models here.

class InventoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    colour = models.TextField(blank=True, null=True)
    quality = models.TextField(blank=True, null=True)
    durability = models.TextField(blank=True, null=True)
    stock_availability = models.TextField(blank=True, null=True)
    category = models.ForeignKey('InventoryCategory', on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return self.name
