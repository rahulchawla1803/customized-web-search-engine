from PyDictionary import PyDictionary
from pymongo import MongoClient

dictionary=PyDictionary()

client = MongoClient()
db = client.webSE
docs = db.indexed_repo_title.find({})

title_clean_combined=[]
for doc in docs:
    title_clean=doc['title_clean']
    title_clean_combined=title_clean_combined+title_clean

title_clean_combined_unique=list(set(title_clean_combined))

synonym_list=[]

for title_word in title_clean_combined_unique:
    synonym_list=dictionary.synonym(title_word)
    if synonym_list is None:
        continue
    synonym_list.append(title_word)
    db.synonym.insert({
        "words":synonym_list
    })
