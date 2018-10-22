from nltk import pos_tag, word_tokenize
from pymongo import MongoClient

token = word_tokenize("rahul chawla mcdonalds pizza Rahul")
tagged_sent = pos_tag(token)
print(tagged_sent)
propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
print(propernouns)
'''
client = MongoClient()
db = client.webSE
docs = db.data.find({})

for doc in docs[56:58]:
    token = word_tokenize(doc['content'])
    tagged_sent = pos_tag(token)
    print(tagged_sent)
    propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
    print(propernouns)
'''
