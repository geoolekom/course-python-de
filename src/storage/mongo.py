from mongoengine import connect

MONGO_URL = "mongodb://root:secret@localhost:27017/"
connect("pythonde", host=MONGO_URL)
