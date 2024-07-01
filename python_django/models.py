# python_django/models.py
from django.db import models

def default_image_url():
    return "https://img.freepik.com/premium-vector/default-image-icon-vector-missing-picture-page-website-design-mobile-app-no-photo-available_87543-11093.jpg?w=1060"

class Home(models.Model):
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    municipality = models.CharField(max_length=255)
    squaremeters = models.DecimalField(max_digits=10, decimal_places=2)
    constructionyear = models.IntegerField()
    energylabel = models.CharField(max_length=10)
    imageurl = models.URLField(default=default_image_url)

    class Meta:
        db_table = 'homes'