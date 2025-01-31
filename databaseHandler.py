import os
import firebase_admin
from firebase_admin import credentials, firestore

# firebase setup
cred = credentials.Certificate(os.environ.get('FIREBASE_CREDENTIALS'))
firebase_admin.initialize_app(cred)
db = firestore.client()

def addPlantToDB(uuid: str, eng_name: str, local_name: str, sci_name: str, family: str, category: str, image_path: str):
    plant_data = {
        'uuid': uuid,
        'english_name': eng_name,
        'local_name': local_name,
        'scientific_name': sci_name,
        'family': family,
        'category': category,
        'image_path': image_path
    }
    db.collection("plants").document(uuid).set(plant_data)

def searchPlantsWhere(where: str, search_term: str):
    plants_ref = db.collection("plants")
    results = plants_ref.where(where, ">=", search_term).stream()
    return [doc.to_dict() for doc in results]

def searchPlants(search_term: str):
    plants_ref = db.collection("plants")
    results = []
    fields = ['english_name', 'local_name', 'scientific_name', 'family', 'category']
    for field in fields:
        query = plants_ref.where(field, ">=", search_term).where(field, "<=", search_term + "\uf8ff").stream()
        results.extend([doc.to_dict() for doc in query])
    return results

def showNewPlants():
    plants_ref = db.collection("plants").stream()
    return [doc.to_dict() for doc in plants_ref]

def showPlant(uuid: str):
    plant_ref = db.collection("plants").document(uuid).get()
    return plant_ref.to_dict() if plant_ref.exists else None

def getSecret():
    return [doc.to_dict() for doc in db.collection(os.environ.get('SECRET')).stream()][0][os.environ.get('KEY')]
