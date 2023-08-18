from mongoengine import connect, disconnect
from pymongo import MongoClient
from load_data import load_authors, load_quotes

# Відключення попереднього з'єднання (якщо таке було)
disconnect()

# Параметри підключення до MongoDB Atlas
mongo_uri = "mongodb+srv://Siia:Dartiana95@mycluster.39vlnle.mongodb.net/BS_Data"

# Підключення до MongoDB Atlas
client = MongoClient(mongo_uri)
db = client["BS_Data"]

# Підключення до mongoengine
connect('BS_Data', host=mongo_uri)


# Завантаження даних з authors.json та quotes.json
authors_data = load_authors("authors.json")
quotes_data = load_quotes("quotes.json")


# Збереження даних у відповідні колекції бази даних
authors_collection = db["authors"]
quotes_collection = db["quotes"]

# Вставка даних у колекції
authors_collection.insert_many(authors_data)
quotes_collection.insert_many(quotes_data)

# Закриття з'єднання з базою даних
client.close()

print("Дані успішно завантажені до хмарної бази даних MongoDB.")

