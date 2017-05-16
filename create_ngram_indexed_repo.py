from ngram import NGram
from pymongo import MongoClient
from general import cleaning
from collections import Counter
from stemming.porter2 import stem


client = MongoClient()
db=client.webSE
docs=db.data1500.find({})

#print("check1")
for doc in docs:
    content=doc['content']
    content_clean=cleaning(content)
    content_clean_root=[]
    for word in content_clean:
        root_word=stem(word)
        content_clean_root.append(root_word)
        #print("check2")

    object_top1=Counter(content_clean_root)
    top_root_object=object_top1.most_common(5)
    top_root_words=[]

    for key,val in top_root_object:
        top_root_words.append(key)
        #print("check3")


    gram2 =[]
    gram3 =[]
    len_content_clean=len(content_clean)
    #print("check4")
    for index, word in enumerate(content_clean):
        if stem(word) in top_root_words:
            if index in [0, 1, 2, len_content_clean-1, len_content_clean-2, len_content_clean-3]:
                continue

            gram2_words=content_clean[index-1] + ' ' + word
            gram2.append(gram2_words)
            gram2_words = word + ' ' + content_clean[index + 1]
            gram2.append(gram2_words)
            #print("check5")

            gram3_words = word + ' ' + content_clean[index + 1] + ' ' + content_clean[index + 2]
            gram3.append(gram3_words)
            gram3_words = content_clean[index - 1] + ' ' + word + ' ' + content_clean[index + 1]
            gram3.append(gram3_words)
            gram3_words = content_clean[index - 2] + ' ' +content_clean[index - 1] + ' ' + word
            gram3.append(gram3_words)
        #print("check6")

    object_top2=Counter(gram2)
    top_gram2_object=object_top2.most_common(5)

    object_top3 = Counter(gram3)
    top_gram3_object = object_top3.most_common(5)

    top_gram2=[]
    top_gram3=[]
    #print("check7")
    for key, val in top_gram2_object:
        top_gram2.append(key)

    for key, val in top_gram3_object:
        top_gram3.append(key)

    #print("check8")
    db.indexed_ngram.insert({
        "url": doc['url'],
        "title": doc['title'],
        "gram1": top_root_words,
        "gram2": top_gram2,
        "gram3": top_gram3
    })




