from django.db import models
from GreenersAccount.models import Greener

# Create your models here.

class Compost(models.Model):
    
    COMPOST_TYPES = (
        ('AnimalManure', 'Animal manure'),
        ('PlantFertilizers', 'Plant-based fertilizers'),
        ('BiodegradableFertilizers', 'Biodegradable fertilizers'),
    )
    
    CompostName = models.CharField(max_length=255)
    CompostImage = models.FileField(upload_to='composts/', null=True, blank=True)
    CompostType = models.CharField(max_length=30, choices=COMPOST_TYPES)

    def __str__(self):
        return self.CompostName

class CompostOffer(models.Model):
    
    
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('expired', 'Expired')
    )

    AnimalManureQuantity = models.IntegerField(blank=True, null=True)
    PlantFertilizersQuantity = models.IntegerField(blank=True, null=True)
    BiodegradableFertilizersQuantity = models.IntegerField(blank=True, null=True)
    StartDate = models.DateField(blank=True)
    EndDate = models.DateField(blank=True, null=True)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_completed')
    Greener = models.ForeignKey(Greener, on_delete=models.CASCADE, related_name='Greener')


