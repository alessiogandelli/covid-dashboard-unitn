from pymongo import MongoClient
client = "mongodb+srv://d8eea:mandarino@cluster0.soxtc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(client)
db = client.covid
model_collection = db.models

def get_by_model(model_name):
    model = list(model_collection.find({"name": model_name}))
    print("Model retrieved from db", model)
    return model

def get_by_region(region_id):
    model = list(model_collection.find({"region_id": region_id}))
    print("Region retrieved from db", model)
    return model
