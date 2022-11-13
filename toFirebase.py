import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
  

f = open('class_info.json')
class_info = json.load(f)

cred_obj = firebase_admin.credentials.Certificate('/Users/williamlee/Desktop/BostonHack/bostonhack-axinio-firebase-adminsdk-jucdk-a6596530ad.json')

default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': "https://bostonhack-axinio-default-rtdb.firebaseio.com/"
	})

ref = db.reference("/")
ref.set({"class_info":class_info})