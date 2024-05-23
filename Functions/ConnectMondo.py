from pymongo import MongoClient

client = MongoClient('mongodb+srv://Example:12345@casa.lvwjpfm.mongodb.net/?retryWrites=true&w=majority&appName=Casa')
db = client["Casa"]
collection = db["Statistics"]

# Buscar documentos con AREA igual a "PTO. VENTA AMERICA"
cursor = collection.find({"AREA": "PTO. VENTA AMERICA"})


documents = list(cursor)
print(documents)
