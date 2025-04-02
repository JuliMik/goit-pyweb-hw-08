import json
from pymongo import MongoClient
from config import MONGO_URI

# Підключення до MongoDB
client = MongoClient(MONGO_URI)
db = client["AuthorsQuotesDB"]
quotes_collection = db["quotes"]
authors_collection = db["authors"]


# Функція для пошуку цитат по імені автора
def search_by_name(author_name):
    author = authors_collection.find_one({"fullname": {"$regex": f"^{author_name}$", "$options": "i"}})

    if author:
        author_id = author["_id"]
        results = quotes_collection.find({"author": author_id})
        results_list = list(results)

        if len(results_list) > 0:
            for result in results_list:
                print(f"Цитата: {result['quote']}")
                print(f"Теги: {', '.join(result['tags'])}")
                print(f"Автор: {author_name}")
                print()
        else:
            print(f"Цитати для автора {author_name} не знайдені.")
    else:
        print(f"Автор {author_name} не знайдений.")


# Функція для пошуку цитат по тегу
def search_by_tag(tag):
    quotes_collection = db["quotes"]
    results = quotes_collection.find({"tags": tag})

    if quotes_collection.count_documents({"tags": tag}) > 0:
        for result in results:
            print(f"{result['author']}: {result['quote']}")
    else:
        print(f"Немає цитат з тегом {tag}.")


# Функція для пошуку цитат по набору тегів
def search_by_tags(tags):
    quotes_collection = db["quotes"]
    tags_list = tags.split(",")
    results = quotes_collection.find({"tags": {"$in": tags_list}})

    if quotes_collection.count_documents({"tags": {"$in": tags_list}}) > 0:
        for result in results:
            print(f"{result['author']}: {result['quote']}")
    else:
        print(f"Немає цитат з тегами {', '.join(tags_list)}.")


# Нескінченний цикл для обробки команд
def main():
    while True:
        user_input = input("Введіть команду: ")

        if user_input.startswith("name:"):
            author_name = user_input.split(":")[1].strip()
            search_by_name(author_name)

        elif user_input.startswith("tag:"):
            tag = user_input[4:].strip()
            search_by_tag(tag)

        elif user_input.startswith("tags:"):
            tags = user_input[5:].strip()
            search_by_tags(tags)

        elif user_input == "exit":
            print("Завершення роботи скрипту.")
            break

        else:
            print("Невірна команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
