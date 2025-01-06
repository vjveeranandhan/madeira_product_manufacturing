from django.db import models
from user_manager.models import CustomUser
from inventory.models import Material
from process.models import Process
# Use CustomUser model for foreign key relationships

class Order(models.Model):
    order_stage = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True, related_name='order_stage')
    product_name = models.CharField(max_length=100)
    product_name_mal = models.TextField(max_length=100, blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    product_description_mal = models.TextField(blank=True, null=True)
    wood = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, related_name='products')  # Assuming Material model exists
    product_length = models.FloatField(help_text="Length in feet")
    product_height = models.FloatField(help_text="Height in feel")
    product_width = models.FloatField(help_text="Width in feet")
    reference_image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    finish =  models.TextField(blank=True, null=True)
    event = models.CharField(max_length=100, blank=True, null=True, help_text="Event associated, e.g., Wedding")
    estimated_delivery_date = models.DateField(blank=True, null=True)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    main_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='managed_products')
    carpenter = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='carpenter_products')
    carpenter_workers = models.ManyToManyField(CustomUser, related_name='carpenter_worker_products', blank=True)
    carpenter_work_hr = models.FloatField(blank=True, null=True, help_text="Work hours required")
    carpenter_work_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carpenter_work_completion_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.product_name
