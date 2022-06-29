from pymongo import MongoClient
client = "mongodb+srv://d8eea:mandarino@cluster0.soxtc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(client)
db = client.covid
model_collection = db.models

def get_model(model_name):
    model = model_collection.find_one({"name": model_name})
    print("Model retrieved from db", model['name'])
    return model
