# -*- coding: utf-8 -*-
import requests
import time

# Wait for the server to start (optional)
time.sleep(10)

url = 'http://127.0.0.1:8000/api/sellhome/'
data = {
    "address": "1234 Main St",
    "price": 500000,
    "municipality": "4700 Næstved",
    "squaremeters": 100,
    "constructionyear": 2015,
    "energylabel": "A",
    "imageurl": "https://example.com/image.jpg"
}

response = requests.post(url, json=data)
print(response.json())