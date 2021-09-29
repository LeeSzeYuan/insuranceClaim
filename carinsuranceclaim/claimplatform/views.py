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
    "vehicle_car_insurance_id":vehicle_car_insurance_id
        

    })