import pyrebase
import requests
import pprint

def get_url(url_type):
    claim_object=database.child('claim').get().val()
    lst=[]
    for key in claim_object:
          car_photo_url=database.child('claim').child(key).child(url_type).get().val()
          lst.append(car_photo_url)
    return lst

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

test_list = get_url("invoice_url")
index_value = similarity("https://firebasestorage.googleapis.com/v0/b/insurtech-hackathonn.appspot.com/o/legit.png?alt=media&token=3b814887-6e01-4a02-a553-40738b1eea81", test_list)

# print(test_list[index_value[0]])

final = database.child('claim').order_by_child('invoice_url').equal_to(test_list[index_value[0]]).get().val()
for key in final:
    print(key)