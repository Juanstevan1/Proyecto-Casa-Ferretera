from pymongo import MongoClient

client = MongoClient('mongodb+srv://Example:12345@casa.lvwjpfm.mongodb.net/?retryWrites=true&w=majority&appName=Casa')

db = client["Casa"]

collection = db["Usuarios"]

dc = collection.find_one({"Nombre": "MARIN LOPEZ MARIA CRISTINA", "cedula": 1020395640})

print(dc)