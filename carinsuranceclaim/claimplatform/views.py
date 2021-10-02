from django.http import request
from django.shortcuts import render
from django.core.files.storage import default_storage
from serpapi import GoogleSearch
import pyrebase
import veryfi
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf


# model=load_model('.models/keras_model.h5')

config  = {
  "apiKey": "AIzaSyBflqWHGwNwcoRtBGKho-4rV83sSDoizgY",
  "authDomain": "insurtech-hackathonn.firebaseapp.com",
  "databaseURL": "https://insurtech-hackathonn-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "insurtech-hackathonn",
  "storageBucket": "insurtech-hackathonn.appspot.com",
  "messagingSenderId": "876544685456",
  "appId": "1:876544685456:web:17a5d78ec66eb9b6b6af15",
}

firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database = firebase.database()
user_id = database.child('vehicle').child('0').get().key()

db=firebase.database()

def post_create(request):
    insurance_id = request.POST.get('insurance_id')
    type_of_accidence = request.POST.get('cars')
    date_of_accidence = request.POST.get('calendar')
    accidence_location = request.POST.get('location_data')
    url = request.POST.get('url')
    invoice_url = request.POST.get('invoice_url')

    file = request.FILES["files"]
    file_name = default_storage.save(file.name, file)
    file_url = default_storage.path(file_name)

    invoice_file = request.FILES["invoice_files"]
    invoice_file_name = default_storage.save(invoice_file.name, invoice_file)
    invoice_file_url = default_storage.path(invoice_file_name)

    # ocr_result = ocr(invoice_file_url)
    # similar_image = image_search(url)
    damage(file_url)
    
    data = {
      "insurance_id":insurance_id, 
      "type_of_accidence":type_of_accidence, 
      "date_of_accidence":date_of_accidence, 
      "accidence_location":accidence_location, 
      "car_url":url, 
      "invoice_url":invoice_url,
      # "ocr_result": ocr_result,
      # "similar_image": similar_image
    }

    database.child('claim').push(data)

    
    return render(request,"claimplatform/after_claim.html",{
      "insurance_id":insurance_id,
      "type_of_accidence":type_of_accidence,
      "date_of_accidence":date_of_accidence,
      "accidence_location":accidence_location,
      "car_url":url,
      "invoice_url":invoice_url
    })




# Create your views here.
def index(request):
    vehicle_model = database.child('vehicle').child('0').child('model').get().val()
    vehicle_registration_number = database.child('vehicle').child('0').child('registration_number').get().val()
    vehicle_year = database.child('vehicle').child('0').child('year').get().val()
    vehicle_car_insurance_id = database.child('vehicle').child('0').child('car_insurance_id').get().val()

    return render(request, "claimplatform/index.html",{
      "vehicle_model":vehicle_model,
      "vehicle_registration_number":vehicle_registration_number,
      "vehicle_year":vehicle_year,
      "vehicle_car_insurance_id":vehicle_car_insurance_id,
      "insurance_id": vehicle_car_insurance_id
    })
    
def table(request):
  return render(request,"claimplatform/table.html")


#function list
def ocr(file_url):
    client_id = "vrfLWsFjUAO3OnyAjOsFXHAdRXclPtApst1tUvO"
    client_secret = "g1Z0XzlXOuBVUAOzDp7IVyWfV1trboXJ2ZUIrCIyKBYEL2GpJlwszFjY3DcWgfy3o6t7N4V5mlXAu0EzgMp0xJ4ZsB0rdKNlCCAmNDOr2LCPJUjL411efoGfkAkWbC1i"
    username = "lsyuan1029"
    api_key = "9e9a239893ff64c881780da0d85f9d69"

    client = veryfi.Client(client_id, client_secret, username, api_key)

    categories = ["Travel", "Airfare", "Lodging", "Job Supplies and Materials", "Grocery", "insurance claim"]
    result = client.process_document(file_url, categories)

    return result

def image_search(img_url):
    params = {
        "engine": "google_reverse_image",
        "image_url": img_url,
        "api_key": "de3ff00136552555a9a290e7e9ef19f7e03b51814d79d2d6cdcff8f47dc9ecbe"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    inline_images = results['inline_images']
    return inline_images[0]

def damage(img_url):
    # model=load_model('claimplatform/keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(img_url)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    predictions = model.predict(data)