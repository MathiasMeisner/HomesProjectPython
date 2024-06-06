# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from .models import Home, default_image_url
import json

@csrf_exempt
def create_home(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_home = Home(
                address=data.get('address'),
                municipality=data.get('municipality'),
                price=data.get('price'),
                squaremeters=data.get('squaremeters'),
                constructionyear=data.get('constructionyear'),
                energylabel=data.get('energylabel'),
                imageurl=data.get('imageurl', default_image_url())
            )
            
            new_home.save()
            return JsonResponse({
                'id': new_home.id,
                'address': new_home.address,
                'municipality': new_home.municipality,
                'price': new_home.price,
                'squaremeters': new_home.squaremeters,
                'constructionyear': new_home.constructionyear,
                'energylabel': new_home.energylabel,
                'imageurl': new_home.imageurl,
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
