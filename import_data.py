import json
from pymongo import MongoClient
from config import MONGO_URI

# Підключення до MongoDB
client = MongoClient(MONGO_URI)
db = client["AuthorsQuotesDB"]

# Імпорт авторів
with open("authors.json", "r", encoding="utf-8") as file:
    authors_data = json.load(file)

authors_collection = db["authors"]

for author in authors_data:
    existing_author = authors_collection.find_one({"fullname": author["fullname"]})
    if not existing_author:
        authors_collection.insert_one(author)
        existing_author = authors_collection.find_one({"fullname": author["fullname"]})  # Отримуємо _id

print("✅ Автори додані!")

# Імпорт цитат
with open("quotes.json", "r", encoding="utf-8") as file:
    quotes_data = json.load(file)

quotes_collection = db["quotes"]

for quote in quotes_data:
    author = authors_collection.find_one({"fullname": quote["author"]})  # Знаходимо автора

    if author:
        quote["author"] = author["_id"]  # Використовуємо _id без ObjectId
        quotes_collection.insert_one(quote)  # Зберігаємо оновлену цитату

print("✅ Цитати додані!")
