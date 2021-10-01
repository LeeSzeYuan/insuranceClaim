from django.http import request
from django.shortcuts import render
import pyrebase

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
database=firebase.database()
user_id = database.child('vehicle').child('0').get().key()

db=firebase.database()

data ={"name":"Khor y Yi"}



def post_create(request):
    user_id= request.POST.get('user_id')
    type_of_accidence= request.POST.get('cars')
    date_of_accidence= request.POST.get('calendar')
    accidence_location= request.POST.get('location_data')
    url=request.POST.get('url')
    invoice_url=request.POST.get('invoice_url')
    
    data={"user_id":user_id,"type_of_accidence":type_of_accidence,"date_of_accidence":date_of_accidence,"accidence_location":accidence_location,"car_url":url,"invoice_url":invoice_url}
    database.child('claim').push(data)
    return render(request,"claimplatform/after_claim.html",{
      "user_id":user_id,"type_of_accidence":type_of_accidence,"date_of_accidence":date_of_accidence,"accidence_location":accidence_location,"car_url":url,"invoice_url":invoice_url
    })




# Create your views here.
def index(request):
    vehicle_model=database.child('vehicle').child('0').child('model').get().val()
    vehicle_registration_number=database.child('vehicle').child('0').child('registration_number').get().val()
    vehicle_year=database.child('vehicle').child('0').child('year').get().val()
    vehicle_car_insurance_id=database.child('vehicle').child('0').child('car_insurance_id').get().val()
    return render(request,"claimplatform/index.html",{
      "vehicle_model":vehicle_model,
      "vehicle_registration_number":vehicle_registration_number,
      "vehicle_year":vehicle_year,
      "vehicle_car_insurance_id":vehicle_car_insurance_id,
      "user_id": user_id
    })

