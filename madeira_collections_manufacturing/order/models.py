from django.db import models
from user_manager.models import CustomUser
from inventory.models import Material
from process.models import Process
# Use CustomUser model for foreign key relationships

class Order(models.Model):
    STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('requested', 'Requested'),
        ('checking', 'Checking'),
        ('completed', 'Completed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    ORDER_STATUS = [
        ('enquiry', 'Enquiry'),
        ('on_going', 'On Going'),
        ('over_due', 'Over due'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ] 
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS,
        default='enquiry'
    )
    current_process = models.ForeignKey(Process, on_delete=models.PROTECT, related_name='order_stage', blank=True, null=True)
    product_name = models.CharField(max_length=100)
    product_name_mal = models.TextField(max_length=100, blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)
    product_description_mal = models.TextField(blank=True, null=True)
    material_ids = models.ManyToManyField(Material, blank=True, related_name='products')
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
    address = models.TextField(blank=True, null=True)
    main_manager_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='managed_products')
    carpenter_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='carpenter_products')
    # carpenter_workers_id = models.ManyToManyField(CustomUser, related_name='carpenter_worker_products', blank=True)
    # carpenter_work_hr = models.FloatField(blank=True, null=True, help_text="Work hours required")
    # carpenter_work_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # carpenter_work_completion_date = models.DateField(blank=True, null=True)
    completed_processes = models.ManyToManyField(Process, blank=True, related_name='process')
    enquiry_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated', help_text="Status of the enquiry")

    # material_length = models.FloatField(help_text="Length in feet", blank=True, null=True)
    # material_height = models.FloatField(help_text="Height in feel", blank=True, null=True)
    # material_width = models.FloatField(help_text="Width in feet",  blank=True, null=True)

    material_cost = models.FloatField(default=0.0)
    ongoing_expense = models.FloatField(default=0.0)
    over_due = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

class OrderImage(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='order_images/')

    def __str__(self):
        return f"Image for {self.order.product_name}"