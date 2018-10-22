from pymongo import MongoClient


client = MongoClient()
db=client.webSE
docs=db.indexed_ngram.find({})

for doc in docs:
    print(type(doc['gram2']))