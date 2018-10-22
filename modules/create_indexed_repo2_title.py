from pymongo import MongoClient
from general import cleaning
from stemming.porter2 import stem

client = MongoClient()
db=client.webSE

docs_count=db.data1500.find({}).count()
docs=db.data1500.find({})
title_combined_unique_root=[]

for doc in docs:
    title=doc['title']
    title_clean = cleaning(title)
    title_clean_root=[]

    for word in title_clean:
        root_word=stem(word)
        title_clean_root.append(root_word)

    title_clean_unique_root=list(set(title_clean_root))

    for word in title_clean_unique_root:
        title_combined_unique_root.append(word)

#print(title_combined_unique_root)

docs=db.data1500.find({})

for doc in docs:

    title_root = []
    title_clean_root=[]
    idf_word_list = []
    title=doc['title']
    title_clean = cleaning(title)

    for word in title_clean:
        root_word=stem(word)
        title_clean_root.append(root_word)

    for title_word in title_clean_root:
        count_title_word = title_combined_unique_root.count(title_word)
        idf_word=docs_count/count_title_word
        idf_word_list.append(idf_word)


    db.indexed_repo_title.insert({
        "url": doc['url'],
        "title":doc['title'],
        "title_clean": title_clean,
        "title_root": title_clean_root,
        "idf_word_list": idf_word_list
    })


