from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()


client = MongoClient('mongodb+srv://Example:12345@casa.lvwjpfm.mongodb.net/?retryWrites=true&w=majority&appName=Casa')

db = client["Casa"]

collection = db["Usuarios"]


async def login(name, password):
    print(name)
    print(password)
    try:
        user=collection.find_one({"Nombre": str(name), "cedula": int(password)})
        print(user)
    except:
        return False
    if(user):
        if(user["Nombre"] == "CASA FERRETERA"):
            return "Admin"
        return True
    return False
