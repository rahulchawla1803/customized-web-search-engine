import random
from pymongo import MongoClient
from random import randint

client = MongoClient()
db=client.webSE
docs=db.data1500.find({})

content_dict={}
list_doc_url=[]
list_random_content_5=[]

for doc in docs:
    doc_content=doc['content']
    doc_url=doc['url']
    list_doc_url.append(doc_url)
    content_dict[doc_url]=doc_content


list_random_url_5 = random.sample(list_doc_url, 5)
#print(list_random_url_5)

for url in list_random_url_5:
    list_random_content_5.append(content_dict[url])

#print(list_random_content_5)


list_combined_query=[]
for i, content in enumerate(list_random_content_5):
    list_content_forloop=content.split()
    #print(list_content_forloop)
    len_list_content_forloop_split=len(list_content_forloop)
    random_int=randint(100,len_list_content_forloop_split-12)
    subset_list_content_forloop=list_content_forloop[random_int:random_int+3]
    list_combined_query.append(subset_list_content_forloop)

print(list_combined_query)

list_combined_query_str=[]
for li in list_combined_query:
    list_combined_query_str.append(' '.join(li))

print(list_combined_query_str)






docs=db.indexed_ngram.find({})

doc_url=[]
doc_gram3=[]
doc_gram2=[]
for doc in docs:
    temp_url=doc['url']
    if temp_url in list_random_url_5:

        doc_url.append(temp_url)
        temp_gram2=doc['gram2']
        doc_gram2.append(temp_gram2)
        temp_gram3 = doc['gram3']
        doc_gram3.append(temp_gram3)

list_combined_query=[]
for url in list_random_url_5:






random_3gram=[]
list_3gram=[]
list_2gram=[]
for doc in docs:
    url=doc['url']
    if url in list_random_url_5:
        random_3gram=random.sample(doc['gram3'],1)
        random_2gram = random.sample(doc['gram2'], 1)
        list_3gram.append(random_3gram)
        list_2gram.append(random_2gram)


#print(list_3gram)
#print(list_2gram)



for i in range(5):
    list_combined_query=list_3gram+list_2gram
    #print(list_combined_query)

























