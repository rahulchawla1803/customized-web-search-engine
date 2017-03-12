from pymongo import MongoClient
from collections import Counter
from stop_words import get_stop_words

def cleaning(content):
    content = content.lower()
    content_clean = []
    temp = []
    words = content.split()
    for j in words:
        if j not in stop_words:
            temp.append(j)

    symbols = "!@#$%^&*(){}[]:;,\"'<>?./+_=.-|"
    for w in temp:
        for i in range(0, len(symbols)):
            w = w.replace(symbols[i], "")
        if len(w) > 0:
            content_clean.append(w)
    return content_clean



stop_words = get_stop_words('english')
client = MongoClient()
db=client.webSE

docs=db.data.find({})
#print(docs[0])
title_combined=[]

for doc in docs:
    title=doc['title']
    title_clean = cleaning(title)
    for word in title_clean:
        title_combined.append(word)

total_len_title=len(title_combined)
#print(total_len_title)
#print(title_combined)

docs=db.data.find({})
for i in docs:
    content=i['content']
    title=i['title']

    title_clean = []
    content_clean = []
    keyword_relative=[]
    title_relative=[]
    keywords=[]
    content_clean=cleaning(content)
    title_clean=cleaning(title)

    for title_word in title_clean:
        count_title=title_combined.count(title_word)
        inverse_count_title=1-(count_title/total_len_title)
        title_relative.append(inverse_count_title)

    len_one_doc=len(content_clean)
    if len_one_doc<100:
        keyword_count=5
    if len_one_doc>=100 and len_one_doc<1000:
        keyword_count=7
    if len_one_doc>=1000:
        keyword_count=10
    x=Counter(content_clean)

    top=x.most_common(keyword_count)
    len_top=len(top)

    sum=0
    for (key,val) in top:
        sum=sum+val
    for (key,val) in top:
        keywords.append(key)
        keyword_relative.append(val/len_one_doc)

    #print("title: " + title)
    #print("title_clean : ", title_clean)
    db.keyword.insert({"url":i['url'], "title_clean":title_clean,"title_relative":title_relative,"keywords":keywords, "keyword_relative":keyword_relative})



def cleaning(content):
    content = content.lower()
    content_clean = []
    temp = []
    words = content.split()
    for j in words:
        if j not in stop_words:
            temp.append(j)

    symbols = "!@#$%^&*(){}[]:;,\"'<>?./+_="
    for w in temp:
        for i in range(0, len(symbols)):
            w = w.replace(symbols[i], "")
        if len(w) > 0:
            content_clean.append(w)
    return content_clean
