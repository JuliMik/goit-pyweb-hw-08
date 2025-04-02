from mongoengine import Document, StringField, BooleanField, connect

# Підключення до MongoDB
connect(db="EmailQueueDB", host="mongodb://localhost:27017/EmailQueueDB")


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    email_sent = BooleanField(default=False)
