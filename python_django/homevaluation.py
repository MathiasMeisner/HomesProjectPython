# -*- coding: utf-8 -*-

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HomesProjectPython.settings')
django.setup()

from django.db.models import F, Avg
from .models import Home
import math

# Function to calculate average sqm price in municipality before valuating a single home

def avg_sqm_price_in_municipality(municipality):
    homes_in_municipality = Home.objects.filter(
        municipality=municipality,
        price__gt=0,
        squaremeters__gt=0
    )

    avg_price_per_square_meter = homes_in_municipality.annotate(
        price_per_sqm=F('price') / F('squaremeters')
    ).aggregate(
        avg_price_per_sqm=Avg('price_per_sqm')
    )['avg_price_per_sqm']

    rounded_avg_price = round(avg_price_per_square_meter or 0)
    return rounded_avg_price

# Function to valuate single home. Values need adjustment in future work

def calculate_single_home(municipality, squaremeters, constructionyear, energylabel):
    avg_price_per_square_meter = avg_sqm_price_in_municipality(municipality)
    total_price = avg_price_per_square_meter * squaremeters

    adjusted_price = total_price

    if constructionyear >= 2013:      
            adjusted_price *= 1.17
    elif 2007 <= constructionyear <= 2012:
            adjusted_price *= 1.10
    elif 1999 <= constructionyear <= 2006:
            adjusted_price *= 1.01
    elif 1979 <= constructionyear <= 1998:
            adjusted_price *= 0.78
    elif 1973 <= constructionyear <= 1978:
            adjusted_price *= 0.82
    elif 1961 <= constructionyear <= 1972:
            adjusted_price *= 0.86
    elif 1951 <= constructionyear <= 1960:
            adjusted_price *= 1.02
    elif 1931 <= constructionyear <= 1950:
            adjusted_price *= 1.27
    elif 1890 <= constructionyear <= 1930:
            adjusted_price *= 1.0
    elif constructionyear < 1890:
            adjusted_price *= 0.88

    energy_label_adjustments = {
        "A": 1.21,
        "B": 1.17,
        "C": 1.1,
        "D": 1,
        "E": 0.93,
        "F": 0.87,
        "G": 0.75
    }

    adjusted_price *= energy_label_adjustments.get(energylabel, 1)

    rounded_adjusted_price = round(adjusted_price, 0)
    return rounded_adjusted_price
