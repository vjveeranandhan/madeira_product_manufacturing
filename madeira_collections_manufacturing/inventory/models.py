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
    STOCK_AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    colour = models.TextField(blank=True, null=True)
    quality = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    durability = models.TextField(blank=True, null=True)
    stock_availability = models.CharField(
        max_length=20,
        choices=STOCK_AVAILABILITY_CHOICES,
        default='in_stock'
    )
    price = models.FloatField(default=0.0)
    category = models.ForeignKey('InventoryCategory', on_delete=models.CASCADE, related_name='materials')

    def __str__(self):
        return self.name
