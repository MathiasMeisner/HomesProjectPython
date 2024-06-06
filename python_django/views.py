# python_django/views.py
from django.http import JsonResponse
from django.db.models import Q
from .models import Home
from .homevaluation import avg_sqm_price_in_municipality, calculate_single_home

def get_sqm_price(request, municipality):
    print(f"Municipality: {municipality}")  # Debugging print statement
    average_price = avg_sqm_price_in_municipality(municipality)
    return JsonResponse(average_price, safe=False)

def get_single_home_price(request, municipality, squaremeters, constructionyear, energylabel):
    adjusted_price = calculate_single_home(
        municipality,
        squaremeters,
        constructionyear,
        energylabel
    )
    return JsonResponse(adjusted_price, safe=False)

# Define valid energy labels
VALID_ENERGY_LABELS = ['G', 'F', 'E', 'D', 'C', 'B', 'A']

def get_homes(request):
    # Get query parameters with default None if not provided
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    min_sqm = request.GET.get('min_sqm')
    max_sqm = request.GET.get('max_sqm')
    
    min_constyear = request.GET.get('min_constyear')
    max_constyear = request.GET.get('max_constyear')
    
    min_energy_label = request.GET.get('min_energy_label')  # New parameter
    max_energy_label = request.GET.get('max_energy_label')  # New parameter
    
    print("Initial number of homes:", Home.objects.count())  # Debugging statement

    # Start with all homes
    homes = Home.objects.all()

    # Filter homes based on price range if provided
    if min_price is not None:
        try:
            homes = homes.filter(price__gte=int(min_price))
        except ValueError:
            pass  # Handle invalid integer input for min_price
    if max_price is not None:
        try:
            homes = homes.filter(price__lte=int(max_price))
        except ValueError:
            pass  # Handle invalid integer input for max_price

    print("Number of homes after price filter:", homes.count())  # Debugging statement

    # Filter square meters
    if min_sqm is not None:
        try:
            homes = homes.filter(squaremeters__gte=int(min_sqm))
        except ValueError:
            pass  # Handle invalid integer input for min_sqm
    if max_sqm is not None:
        try:
            homes = homes.filter(squaremeters__lte=int(max_sqm))
        except ValueError:
            pass  # Handle invalid integer input for max_sqm
        
    print("Number of homes after square meter filter:", homes.count())  # Debugging statement
        
    # Filter construction year
    if min_constyear is not None:
        try:
            homes = homes.filter(constructionyear__gte=int(min_constyear))
        except ValueError:
            pass  # Handle invalid integer input for min_constyear
    if max_constyear is not None:
        try:
            homes = homes.filter(constructionyear__lte=int(max_constyear))
        except ValueError:
            pass  # Handle invalid integer input for max_constyear

    print("Number of homes after construction year filter:", homes.count())  # Debugging statement

    # Filter energy label range
    if min_energy_label is not None and max_energy_label is not None:
        # Ensure energy labels are valid and within range
        min_energy_label = min_energy_label.upper()
        max_energy_label = max_energy_label.upper()
        if min_energy_label in VALID_ENERGY_LABELS and max_energy_label in VALID_ENERGY_LABELS:
            homes = homes.filter(energylabel__gte=max_energy_label, energylabel__lte=min_energy_label)

    print("Number of homes after energy label filter:", homes.count())  # Debugging statement

    # Convert filtered homes to JSON format
    homes_data = [
        {
            'id': home.id, 
            'address': home.address, 
            'municipality': home.municipality, 
            'price': home.price, 
            'squaremeters': home.squaremeters, 
            'constructionyear': home.constructionyear, 
            'energylabel': home.energylabel, 
            'imageurl': home.imageurl
        } 
        for home in homes
    ]
    
    return JsonResponse(homes_data, safe=False)

