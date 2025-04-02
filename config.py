import configparser

# Створюємо об'єкт парсера
config = configparser.ConfigParser()
config.read("config.ini")

# Отримуємо URI з файлу конфігурації
MONGO_URI = config["database"]["MONGO_URI"]
