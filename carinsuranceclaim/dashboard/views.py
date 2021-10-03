from django.shortcuts import render
import pyrebase
import requests

# Create your views here.
def index(request):
    return render(request, "dashboard/index.html")


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
auth=firebase.auth()
database=firebase.database()

def details(request,claim_no):

    ClaimNo=database.child('claim').child(claim_no).get().key()
    insurance_id=database.child('claim').child(claim_no).child('insurance_id').get().val()
    user_id=database.child('car_insurance').child(insurance_id).child('user_id').get().val()
    NAME=database.child('users').child(user_id).child('name').get().val()
    INSURANCENUMBER=database.child('claim').child(claim_no).child('insurance_id').get().val()
    Driver_age=database.child('users').child(user_id).child('age').get().val()
    Driver_phone_number=database.child('users').child(user_id).child('phone_number').get().val()
    Driver_address=database.child('users').child(user_id).child('address').get().val()
    Date_of_loss=database.child('claim').child(claim_no).child('date_of_accidence').get().val()
    Place_of_loss=database.child('claim').child(claim_no).child('accidence_location').get().val()
    Circumstance=database.child('claim').child(claim_no).child('type_of_accidence').get().val()
    # Registration_number=database.child('vehicle').order_by_child("car_insurance_id").equal_to(INSURANCENUMBER).get().val()['0']['registration_number']
    # Brand=database.child('vehicle').order_by_child("car_insurance_id").equal_to(INSURANCENUMBER).get().val()['0']['brand']
    # Model=database.child('vehicle').order_by_child("car_insurance_id").equal_to(INSURANCENUMBER).get().val()['0']['model']
    # Year=database.child('vehicle').order_by_child("car_insurance_id").equal_to(INSURANCENUMBER).get().val()['0']['year']

    ocr_result = database.child('claim').child(claim_no).child('ocr_result').get().val()

    DATE_OF_=database.child('claim').child('-Mkv6-mXxnfNWYTEfMpq').child('invoice_url').get().val()
    claim_data = database.child('claim').child(claim_no).get().val()
    confidenc = database.child('claim').child(claim_no).child('confidenc').get().val()
    confidenc = float(confidenc)
    confidenc *= 100
    # similar_claim = database.child('claim').child(similar_claim).get().val()

    # if (similar_claim == null) {
    #   imageList = get_url("invoice_url")
    #   result["max_index"], max_value = similarity(claim_data)
    # }

    return render(request,"dashboard/details.html",{
      "ClaimNo":ClaimNo,
      "NAME":NAME,
      "CLIENTNUMBER":user_id,
      "INSURANCENUMBER":INSURANCENUMBER,
    #   "DATE_OF_CLAIM": DATE_OF_CLAIM
      "Driver_name":NAME,
      "Driver_age":Driver_age,
      "Driver_phone_number":Driver_phone_number,
      "Driver_address":Driver_address,
      "Date_of_loss":Date_of_loss,
      "Place_of_loss":Place_of_loss,
      "Circumstance":Circumstance,
      # "Registration_number":Registration_number,
      # "Brand":Brand,
      # "Model":Model,
      # "Year":Year,  
      "ocr_result": ocr_result,
      "claim_data": claim_data,
      "confidenc": confidenc
    })



