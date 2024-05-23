from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()


client = MongoClient('mongodb+srv://Example:12345@casa.lvwjpfm.mongodb.net/?retryWrites=true&w=majority&appName=Casa')

db = client["Casa"]



async def login(name, password):
    
    collection = db["Usuarios2"]
    try:
        user=collection.find_one({"Nombre": str(name), "cedula": int(password)})
        print(user)
    except:
        return False
    if(user):
        if(user["Nombre"] == "CASA FERRETERA"):
            return "admin"
        print(user)
        return user['Nombre']
    return False


async def Selfromdb(name:str):
    collection = db["Statistics2"]
    collection2=db['Usuarios2']
    area=collection2.find_one({'Nombre':name})['Area']
    result1 = collection.find({"Nombre":str(name)})
    result2=collection.find({'Area':area})
    result=list(result1)+list(result2)
    return list(result)
    
