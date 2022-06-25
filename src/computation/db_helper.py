#%%
from pymongo import MongoClient
client = "mongodb+srv://d8eea:mandarino@cluster0.soxtc.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(client)
db = client.covid
model_collection = db.models
# %%
model_collection.insert_one({'name' : 'positive' ,'intercept': 1234, 'coefficients': [1,2,3,4]})
# %%

def save_model(model):
    model_collection.insert_one(model)
    print("Model saved ", model['name'])
