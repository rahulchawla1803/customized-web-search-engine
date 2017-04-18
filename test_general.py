from pymongo import MongoClient

client = MongoClient()
db=client.webSE
docs=db.health.find({})

links=[]

for doc in docs:
    links.append(doc['url'])
    print(doc['url'])



print(len(links))
print(len(list(set(links))))



