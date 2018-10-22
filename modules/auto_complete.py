from pymongo import MongoClient

def auto():
    list_auto_complete=[]
    client = MongoClient()
    db = client.webSE
    docs = db.indexed_ngram.find({})

    for doc in docs:
        for doc_word_gram2 in doc['gram2']:
            list_auto_complete.append(doc_word_gram2)
        for doc_word_gram3 in doc['gram3']:
            list_auto_complete.append(doc_word_gram3)

    set_auto_complete=set(list_auto_complete)
    list_auto_complete_unique=list(set_auto_complete)

    return list_auto_complete_unique

