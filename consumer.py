import pika
import json
from models import Contact

# Налаштування RabbitMQ
rabbitmq_host = "localhost"
queue_name = "email_queue"


# Функція-заглушка для відправки email
def send_email(contact):
    print(f"[✔] Email sent to {contact.fullname} ({contact.email})")
    contact.email_sent = True
    contact.save()


# Функція обробки повідомлень
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message["contact_id"]

    # Отримуємо контакт із бази даних
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.email_sent:
        send_email(contact)
    else:
        print(f"[!] Contact {contact_id} not found or already notified.")

    # Підтверджуємо обробку повідомлення
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Декларуємо чергу
channel.queue_declare(queue=queue_name, durable=True)

# Обробник отримання повідомлень
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

print("[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
