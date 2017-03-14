from pymongo import MongoClient
from collections import Counter
from general import cleaning
import operator

def search(search_query):
    print(search_query)
    clean_query = cleaning(search_query)
    title_rank={}
    keyword_rank={}
    client = MongoClient()
    db=client.webSE
    docs=db.keyword.find({})

    for doc in docs[0:15]:
        title_match_value=0
        for index,title_keyword in enumerate(doc['title_clean']):
            for query_keyword in clean_query:
                #print("title_keyword : "+ title_keyword+",  query_keyword : "+query_keyword)
                if title_keyword == query_keyword:
                    #print("check loop")
                    title_match_value = title_match_value + doc['title_relative'][index]
        #print(title_match_value)

        title_rank[doc['url']]=title_match_value

    print(title_rank)

    docs=db.keyword.find({})


    for doc in docs[0:15]:
        keyword_match_value=0
        for index , keyword in enumerate(doc['keywords']):
            for query_keyword in clean_query:

                if keyword == query_keyword:
                    keyword_match_value = keyword_match_value + doc['keyword_relative'][index]

        keyword_rank[doc['url']]=keyword_match_value

    #print(keyword_rank)

    combined_rank_dict={}
    for key, value in title_rank.items():
        combined_rank_dict[key]=keyword_rank[key]+value

    #print(combined_rank_dict)

    combined_rank_dict_sorted={}
    for key, value in sorted(combined_rank_dict.items(), key=operator.itemgetter(1), reverse=True):
        if value>0:
            combined_rank_dict_sorted[key] = value

    #print(combined_rank_dict_sorted)

    combined_rank_sorted=[]
    for key in combined_rank_dict_sorted:
        combined_rank_sorted.append(key)

    #print(combined_rank_sorted)


    docs = db.data.find({'url': { '$in': combined_rank_sorted }})
    final_link_title_dict = {}
    #print(combined_rank_sorted)

    doc_dict={}
    for doc in docs:
        doc_dict[doc['url']]=doc['title']

    for link in combined_rank_sorted:
        for (key,value) in doc_dict.items():
            if link==key:
                final_link_title_dict[key]=value

    return final_link_title_dict


#search("videos lower case")