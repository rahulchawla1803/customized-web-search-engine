import random
from pymongo import MongoClient
from random import randint
import query_module
import ranking_text_mining
import ranking_nlp
import combined_ranking

client = MongoClient()
db=client.webSE
docs=db.data1500.find({})

content_dict={}
list_doc_url=[]
list_random_content_50=[]

for doc in docs:
    doc_content=doc['content']
    doc_url=doc['url']
    list_doc_url.append(doc_url)
    content_dict[doc_url]=doc_content
'''
docs=db.data1500.find({})
for doc in docs[1002:1503]:
    doc_content=doc['content']
    doc_url=doc['url']
    list_doc_url.append(doc_url)
    content_dict[doc_url]=doc_content

docs=db.data1500.find({})
for doc in docs[1000:1050]:
    doc_content=doc['content']
    doc_url=doc['url']
    list_doc_url.append(doc_url)
    content_dict[doc_url]=doc_content
'''
list_random_url_50 = random.sample(list_doc_url, 10)
#print(list_random_url_50)

for url in list_random_url_50:
    list_random_content_50.append(content_dict[url])

#print(list_random_url_50)
#print(list_random_content_50)

#for x in list_random_content_50:
    #print(x)

list_combined_query=[]
for content in list_random_content_50:
    list_content_forloop=content.split()
    #print(list_content_forloop)
    len_list_content_forloop_split=len(list_content_forloop)
    random_int=randint(1,len_list_content_forloop_split-10)
    subset_list_content_forloop=list_content_forloop[random_int:random_int+2]
    list_combined_query.append(subset_list_content_forloop)

#print(list_combined_query)

list_combined_query_str=[]
for li in list_combined_query:
    list_combined_query_str.append(' '.join(li))

#print(list_combined_query_str)

docs=db.indexed_ngram.find({})
list_object=[]

for doc in docs:
    temp_url=doc['url']
    if temp_url in list_random_url_50:
        temp_gram2 = doc['gram2']
        temp_gram3 = doc['gram3']
        obj={"url":temp_url, "gram2":temp_gram2, "gram3":temp_gram3}
        list_object.append(obj)

#print(list_object)
list_random_gram2=[]
list_random_gram3=[]

for url in list_random_url_50:
    for object in list_object:
        if url == object['url']:

            gram2_list=object['gram2']
            gram2=random.choice(gram2_list)
            list_random_gram2.append(gram2)

            gram3_list=object['gram3']
            gram3 = random.sample(gram3_list,3)
            gram3=' '.join(gram3)
            #gram3=random.choice(gram3_list)
            list_random_gram3.append(gram3)

#print(list_random_gram2)
#print(list_random_gram3)

list_final_query=[]

for i in range(10):
    temp=[]
    temp.append(list_combined_query_str[i])
    temp.append(list_random_gram2[i])
    temp.append(list_random_gram3[i])
    temp=' '.join(temp)
    list_final_query.append(temp)


#print(list_final_query)
#print(list_random_url_50)

count=0
for iter, temp_query in enumerate(list_final_query):
    query = temp_query
    a, b, c = query_module.query_structure(query)
    result_tm = ranking_text_mining.ranking(a, b, c)
    result_nlp, ngram_considered = ranking_nlp.rank_ngram(query)
    result, result_score = combined_ranking.ranking(result_tm, result_nlp)
    #result=result[:3]
    print(result)
    print(list_random_url_50[iter])

    if list_random_url_50[iter] in result:
        count=count+1
        print("Count=", count)

print("Count=", count)
