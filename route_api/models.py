from django.db import models

# Create your models here.
class FuelStation(models.Model):
    opis_id=models.IntegerField()
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    state = models.CharField(max_length=70)
    rack_id=models.IntegerField()
    price_per_gallon=models.FloatField()
    latitude=models.FloatField(null=True, blank=True)
    longitude=models.FloatField(null=True, blank=True)



    class Meta:
        verbose_name = "Fuel Station"
        verbose_name_plural = "Fuel Stations"
        indexes = [
            models.Index(fields=["price_per_gallon"]),
        ]

        
    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"

