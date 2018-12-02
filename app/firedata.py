import firebase_admin
from firebase_admin import firestore

project_id='yhack-smartcar'

cred = firebase_admin.credentials.Certificate('yhack-smartcar-b905088e1d5c.json')
firebase_app = firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()
