import pika
import json
from faker import Faker
from models import Contact

# Налаштування RabbitMQ
rabbitmq_host = "localhost"
queue_name = "email_queue"

# Генератор фейкових даних
fake = Faker()

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue=queue_name, durable=True)


# Генерація та запис контактів у MongoDB
def generate_contacts(n=10):
    contacts = []
    for _ in range(n):
        contact = Contact(fullname=fake.name(), email=fake.email())
        contact.save()
        contacts.append(contact)

        message = json.dumps({"contact_id": str(contact.id)})
        channel.basic_publish(exchange="", routing_key=queue_name, body=message,
                              properties=pika.BasicProperties(delivery_mode=2))  # Робимо повідомлення збереженим
        print(f"[x] Contact {contact.fullname} ({contact.email}) added to queue")

    return contacts


# Генеруємо 10 контактів та додаємо у чергу
generate_contacts(10)

# Закриваємо з'єднання
connection.close()
