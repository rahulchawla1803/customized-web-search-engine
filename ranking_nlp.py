from ngram import NGram
from pymongo import MongoClient
from general import cleaning
import operator


def rank_ngram(query):
    ngram_analyse=[]
    clean_query=cleaning(query)
    length_query=len(clean_query)
    if length_query is 1:
        return {}, {}

    client = MongoClient()
    db = client.webSE
    docs = db.indexed_ngram.find({})

    rank_sum_dict = {}
    for doc in docs:
        rank_sum_dict[doc['url']]=0

    query_gram2=[]
    for index, word in enumerate(clean_query):
        if index is length_query-1:
            break
        two_word=word + ' ' + clean_query[index+1]
        query_gram2.append(two_word)

    #print(query_gram2)

    query_gram3 = []
    for index, word in enumerate(clean_query):
        if index is length_query - 2:
            break
        three_word = word + ' ' + clean_query[index + 1]+ ' ' + clean_query[index + 2]
        query_gram3.append(three_word)

    #print(query_gram3)

    docs = db.indexed_ngram.find({})
    for doc in docs:
        for query_word_gram2 in query_gram2:
            for doc_word in doc['gram2']:
                if NGram.compare(query_word_gram2, doc_word) >= 0.5:
                    rank_sum_dict[doc['url']] = rank_sum_dict[doc['url']] + 1
                    ngram_analyse.append(doc_word)


    ngram_analyse=list(set(ngram_analyse))
    docs = db.indexed_ngram.find({})
    for doc in docs:
        for query_word_gram3 in query_gram3:
            for doc_word in doc['gram3']:
                if NGram.compare(query_word_gram3, doc_word) >= 0.5:
                    rank_sum_dict[doc['url']]=rank_sum_dict[doc['url']]+3
                    ngram_analyse.append(doc_word)

    ngram_analyse = list(set(ngram_analyse))
    #print(rank_sum_dict)
    rank_sum_dict_unsorted = {}
    for key, value in rank_sum_dict.items():
        if value > 0:
            rank_sum_dict_unsorted[key] = value

    return rank_sum_dict_unsorted, ngram_analyse



#rank_ngram("treatment of breast cancer in this world")
