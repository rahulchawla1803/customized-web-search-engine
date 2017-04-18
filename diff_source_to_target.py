from pymongo import MongoClient

client = MongoClient()
db=client.webSE

docs=db.hindustantimes.find({})


for doc in docs:
    db.data.insert({"url": doc['url'], "title": doc['title'], "content": doc['content']})