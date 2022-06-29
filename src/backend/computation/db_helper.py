#%%
from pymongo import MongoClient
client = "mongodb+srv://d8eea:mandarino@cluster0.soxtc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(client)
db = client.covid
model_collection = db.models
# %%
# %%

def save_model(model):
    model_collection.insert_one(model)
    print("Model saved ", model['name'])
