from pymongo import MongoClient
from collections import Counter
from general import cleaning
import operator
import enchant
from stemming.porter2 import stem
from PyDictionary import PyDictionary



def search(search_query):
    dict = enchant.Dict("en_UK")
    dictionary = PyDictionary()
    print(search_query)
    clean_query = cleaning(search_query)
    synonyms=[]
    synonyms_final=[]
    synonyms_final_root=[]
    for word in clean_query:
        if dict.check(word):
            synonyms=dictionary.synonym(word)
            synonyms_final=synonyms_final+synonyms


    length_clean_query = len(clean_query)
    for word in clean_query[:length_clean_query + 1]:
        suggestions = dict.suggest(word)
        for i in suggestions:
            clean_query.append(i)
    print(clean_query)
    clean_query_root=[]

    for word in clean_query:
        root_word=stem(word)
        clean_query_root.append(root_word)

    for word in synonyms_final:
        root_word=stem(word)
        synonyms_final_root.append(root_word)

    clean_query_root=clean_query_root+synonyms_final_root

    title_rank={}
    keyword_rank={}
    client = MongoClient()
    db=client.webSE
    docs=db.keyword.find({})

    for doc in docs:
        title_match_value=0
        for index,title_keyword_root in enumerate(doc['title_root']):
            for query_keyword_root in clean_query_root:
                #print("title_keyword : "+ title_keyword+",  query_keyword : "+query_keyword)
                if title_keyword_root == query_keyword_root:
                    #print("check loop")
                    title_match_value = title_match_value + doc['title_relative'][index]
        #print(title_match_value)


        title_rank[doc['url']]=title_match_value

    print(title_rank)

    docs=db.keyword.find({})


    for doc in docs:
        keyword_match_value=0
        for index , keyword_root in enumerate(doc['keyword_root']):
            for query_keyword_root in clean_query_root:

                if keyword_root == query_keyword_root:
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


#search("")