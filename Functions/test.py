from pymongo import MongoClient

client = MongoClient('mongodb+srv://root:12345@cluster0.jyuzous.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client["db"]

collection = db["coll"]

dc = collection.find_one({"Nombre": "MARIN LOPEZ MARIA CRISTINA", "cedula": 1020395640})