from pymongo import MongoClient
import operator


def ranking(clean_query_root, query_synonym_root, query_suggestion_root):

    title_rank = {}
    client = MongoClient()
    db = client.webSE
    docs = db.indexed_repo_title.find({})

    for doc in docs:
        title_match_value = 0
        for index, title_word_root in enumerate(doc['title_root']):

            for query_word_root in clean_query_root:
                if title_word_root == query_word_root:
                    title_match_value = title_match_value + doc['idf_word_list'][index]

            for query_word_synonym_root in query_synonym_root:
                if title_word_root == query_word_synonym_root:
                    title_match_value = title_match_value + 0.75*doc['idf_word_list'][index]

            for query_word_suggestion_root in query_suggestion_root:
                if title_word_root == query_word_suggestion_root:
                    title_match_value = title_match_value + 0.5*doc['idf_word_list'][index]

        title_rank[doc['url']] = title_match_value


    title_sorted_rank_dict={}

    for key, value in sorted(title_rank.items(), key=operator.itemgetter(1), reverse=True):
        if value > 0:
            title_sorted_rank_dict[key] = value


    title_sorted_rank_list = []
    for key in title_sorted_rank_dict:
        title_sorted_rank_list.append(key)



    docs = db.indexed_repo_title.find({'url': {'$in': title_sorted_rank_list}})
    link_title_sorted_dict = {}

    doc_dict = {}
    for doc in docs:
        doc_dict[doc['url']] = doc['title']

    for link in title_sorted_rank_list:
        for (key, value) in doc_dict.items():
            if link == key:
                link_title_sorted_dict[key] = value
    print(link_title_sorted_dict)
    return link_title_sorted_dict

