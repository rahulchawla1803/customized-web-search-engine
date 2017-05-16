from pymongo import MongoClient
import operator

def ranking(link_dict_tm, link_dict_nlp):

    #print(link_dict_tm)
    #print(link_dict_nlp)
    link_dict_combined=link_dict_tm

    for key_nlp, value_nlp in link_dict_nlp.items():
        if key_nlp in link_dict_combined:
            link_dict_combined[key_nlp]=link_dict_combined[key_nlp]+value_nlp
        else:
            link_dict_combined[key_nlp]=value_nlp

    link_dict_combined_sorted={}
    ct=0

    for key, value in sorted(link_dict_combined.items(), key=operator.itemgetter(1), reverse=True):
        if ct>=10:
            break
        ct=ct+1
        link_dict_combined_sorted[key] = value

    #print(link_dict_combined_sorted)
    link_list_sorted=[]

    for key in link_dict_combined_sorted:
        link_list_sorted.append(key)


    client = MongoClient()
    db = client.webSE
    docs = db.indexed_repo_title.find({'url': {'$in': link_list_sorted}})

    link_final_sorted_dict = {}
    doc_dict = {}
    for doc in docs:
        doc_dict[doc['url']] = doc['title']

    for link in link_list_sorted:
        for (key, value) in doc_dict.items():
            if link == key:
                link_final_sorted_dict[key] = value
    #print(link_final_sorted_dict)

    return link_final_sorted_dict, link_dict_combined_sorted