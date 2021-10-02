from django.shortcuts import render
import pyrebase

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
    INSURANCENUMBER=database.child('vehicle').child('0').child('car_insurance_id').get().val()

    # DATE_OF_=database.child('claim').child('-Mkv6-mXxnfNWYTEfMpq').child('invoice_url').get().val()
    return render(request,"dashboard/details.html",{
      "ClaimNo":ClaimNo,
      "NAME":NAME,
      "CLIENTNUMBER":user_id,
      "INSURANCENUMBER":INSURANCENUMBER 
    #   "DATE_OF_CLAIM": DATE_OF_CLAIM
    })
