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
import requests
from tensorflow import Graph

model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
      model = load_model(default_storage.path("keras_model.h5"))

model_class = ["Normal Bumper", "Damaged Bumper", "Normal Windshield", "Damaged Windshield", "Normal Door","Damaged Door"]

config  = {
  "apiKey": "AIzaSyBflqWHGwNwcoRtBGKho-4rV83sSDoizgY",
  "authDomain": "insurtech-hackathonn.firebaseapp.com",
  "databaseURL": "https://insurtech-hackathonn-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "insurtech-hackathonn",
  "storageBucket": "insurtech-hackathonn.appspot.com",
  "messagingSenderId": "876544685456",
  "appId": "1:876544685456:web:17a5d78ec66eb9b6b6af15",
}

# list_of_invoice_url = get_url("invoice_url")

firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database = firebase.database()
user_id = database.child('vehicle').child('0').get().key()
db=firebase.database()

def get_url(url_type):
    claim_object=database.child('claim').get().val()
    lst=[]
    for key in claim_object:
          car_photo_url=database.child('claim').child(key).child(url_type).get().val()
          lst.append(car_photo_url)
    return lst



list_of_invoice_url = get_url("invoice_url")

def post_create(request):
    username = request.POST.get('username')
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

    ocr_result = ""
    similar_image = ""
    prediction=""
    claim_status = ""
    similar_claim_id = ""
    similar_claim_url = ""

    ocr_result = ocr(invoice_file_url)
    prediction=damage(file_url)

    if username=="jane":
      similar_image = ""
      claim_status = "approved"
    else:
      similar_image = image_search(url)
      index_value = similarity(invoice_url, list_of_invoice_url)
      final = database.child('claim').order_by_child('invoice_url').equal_to(list_of_invoice_url[index_value[0]]).get().val()
      for key in final:
        similar_claim_id = key
        similar_claim_url = list_of_invoice_url[index_value[0]]
      claim_status = "pending"
    
    
    data = {
      "insurance_id":insurance_id, 
      "type_of_accidence":type_of_accidence, 
      "date_of_accidence":date_of_accidence, 
      "accidence_location":accidence_location, 
      "car_url":url, 
      "invoice_url":invoice_url,
      "ocr_result": ocr_result,
      "similar_image": similar_image,
      "prediction": model_class[prediction[0]],
      "confidenc": str(prediction[1]),
      "claim_status": claim_status,
      "similar_claim_id": similar_claim_id,
      "similar_claim_url": similar_claim_url
    }

    database.child('claim').push(data)

    
    return render(request,"claimplatform/after_claim.html",{
      "claim_status": claim_status,
      "insurance_id":insurance_id,
      "type_of_accidence":type_of_accidence,
      "date_of_accidence":date_of_accidence,
      "accidence_location":accidence_location,
      "car_url":url,
      "invoice_url":invoice_url,
    })




# Create your views here.
def index(request):
    vehicle_model = database.child('vehicle').child('0').child('model').get().val()
    vehicle_registration_number = database.child('vehicle').child('0').child('registration_number').get().val()
    vehicle_year = database.child('vehicle').child('0').child('year').get().val()
    vehicle_car_insurance_id = database.child('vehicle').child('0').child('car_insurance_id').get().val()

    return render(request, "claimplatform/index.html",{
      "username": "jane",
      "vehicle_model":vehicle_model,
      "vehicle_registration_number":vehicle_registration_number,
      "vehicle_year":vehicle_year,
      "vehicle_car_insurance_id":vehicle_car_insurance_id,
      "insurance_id": vehicle_car_insurance_id
    })

def user(request):
    vehicle_model = database.child('vehicle').child('1').child('model').get().val()
    vehicle_registration_number = database.child('vehicle').child('1').child('registration_number').get().val()
    vehicle_year = database.child('vehicle').child('1').child('year').get().val()
    vehicle_car_insurance_id = database.child('vehicle').child('1').child('car_insurance_id').get().val()

    return render(request, "claimplatform/index.html",{
      "username": "christy",
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
    with model_graph.as_default():
        with tf_session.as_default():
          predictions = model.predict(data)
    return [np.argmax(predictions), np.max(predictions)]



def similarity(img1, list): 
  result = []
  for img2 in list:
    r = requests.post(
        "https://api.deepai.org/api/image-similarity",
        data={
            'image1': img1,
            'image2': img2,
        },
        headers={'api-key': '1589c657-6b81-441f-a0b2-acc9ad3155d1'}
    )
    value = r.json()
    result.append(value["output"]["distance"])
  max_value = max(result)
  max_index = result.index(max_value)
  
  return [max_index, max_value]