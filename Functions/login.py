from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()


client = MongoClient('mongodb+srv://Example:12345@casa.lvwjpfm.mongodb.net/?retryWrites=true&w=majority&appName=Casa')

db = client["Casa"]



async def login(name, password):
    
    collection = db["Usuarios"]
    try:
        user=collection.find_one({"Nombre": str(name), "cedula": int(password)})
        print(user)
    except:
        return False
    if(user):
        if(user["Nombre"] == "CASA FERRETERA"):
            return "Admin"
        print(user)
        return user['Area']
    return False


async def Selfromdb(Area):
    collection = db["Statistics"]
    result = collection.find({"AREA":str(Area)})
    return list(result)
    
