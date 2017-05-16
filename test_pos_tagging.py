import nltk
from pymongo import MongoClient
from general import cleaning

client = MongoClient()
db=client.webSE
docs=db.data1500.find({})


for doc in docs[570:575]:
    content=doc['content']
    list_content=cleaning(content)
    str_content=' '.join(list_content)
    text = nltk.word_tokenize(str_content)
    x=nltk.pos_tag(text)

    for i,j in x:
        if j is 'NNP' or j is 'NNPS':
            print(i,j)