# python_django/views.py
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Q
from .models import Home
from .homevaluation import avg_sqm_price_in_municipality, calculate_single_home
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import UserRegisterForm
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
import json

@login_required
def user_info_view(request):
    user = request.user
    user_info = {
        "username": user.username,
        "email": user.email,
        "is_authenticated": user.is_authenticated
    }
    print(f"User info: {user_info}")  # Log user info to the backend terminal
    return JsonResponse(user_info)

def get_user(request):
    user = request.user
    return JsonResponse({'username': user.username})

def user_view(request):
    user = get_user(request)
    if user.is_authenticated:
        return JsonResponse({'username': user.username})
    else:
        return JsonResponse({'username': None}, status=200)

@ensure_csrf_cookie
def set_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

def home_view(request):
    return render(request, 'home.html')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")  # Print the received data for debugging
            form = UserCreationForm(data)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return JsonResponse({"message": "Registration successful"})
            else:
                print(f"Form errors: {form.errors.as_json()}")  # Print form errors for debugging
                return HttpResponseBadRequest(form.errors.as_json())
        except Exception as e:
            print(f"Error processing request: {e}")
            return HttpResponseBadRequest({"error": str(e)})
    else:
        return HttpResponseBadRequest({"error": "Invalid request method"})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"})
            else:
                return HttpResponseBadRequest({"error": "Invalid credentials"})
        except Exception as e:
            return HttpResponseBadRequest({"error": str(e)})
    else:
        return HttpResponseBadRequest({"error": "Invalid request method"})

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"message": "Logout successful"})
    return JsonResponse({"error": "Invalid request method"}, status=400)

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
    
    min_energy_label = request.GET.get('min_energy_label')
    max_energy_label = request.GET.get('max_energy_label')
    
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