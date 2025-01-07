from django.db import models
from user_manager.models import CustomUser
from inventory.models import Material
# Create your models here.
class Process(models.Model):
    name = models.CharField(max_length=100, unique=True)  # English name, must be unique
    name_mal = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)  # Description in English
    description_mal = models.TextField(blank=True, null=True) 
    def __str__(self):
        return self.name

class ProcessDetails(models.Model):
    PROCESS_STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    order_id = models.ForeignKey(
        'order.Order',  # String reference
        on_delete=models.CASCADE,
        related_name='process_details',
        help_text="Reference to the related order"
    )
    process_id = models.ForeignKey(
        'process.Process',  # String reference
        on_delete=models.CASCADE,
        related_name='process_details',
        help_text="Reference to the process"
    )
    main_manager_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='main_managed_processes',
        help_text="Main manager responsible for this process"
    )
    process_manager_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='managed_processes',
        help_text="Manager overseeing this process"
    )
    process_workers_id = models.ManyToManyField(
        CustomUser,
        related_name='worker_processes',
        help_text="Workers involved in the process"
    )
    process_status = models.CharField(
        max_length=20,
        choices=PROCESS_STATUS_CHOICES,
        default='requested',
        help_text="Current status of the process"
    )
    expected_completion_date = models.DateField(
        help_text="Expected date of process completion"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total price for the process"
    )
    image = models.ImageField(
        upload_to='process_images/',
        blank=True,
        null=True,
        help_text="Image related to the process"
    )

    def __str__(self):
        return f"Process Details for Order {self.order_id.id} - Process {self.process_id.id}"
    
class ProcessMaterials(models.Model):
    process_details_id = models.ForeignKey(
        ProcessDetails,
        on_delete=models.CASCADE,
        related_name='process_materials',
        help_text="Reference to the process details"
    )
    material_id = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name='process_materials',
        help_text="Reference to the material"
    )
    material_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of the material"
    )

    def __str__(self):
        return f"Material {self.material_id.id} for Process {self.process_details_id.id}"