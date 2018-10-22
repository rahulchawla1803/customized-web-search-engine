from pymongo import MongoClient
from random import randint

client = MongoClient()
db=client.webSE
docs=db.indexed_ngram.find({})

for doc in docs[1002:1503]:
