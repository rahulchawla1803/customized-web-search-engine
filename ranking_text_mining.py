from pymongo import MongoClient
import operator


def ranking(clean_query_root, query_synonym_root, query_suggestion_root):

    title_rank = {}
    client = MongoClient()
    db = client.webSE
    docs = db.indexed_repo_title.find({})
    number_pages=1503
    max_value=1
    normalization_factor=max_value/number_pages

    for doc in docs:
        title_match_value = 0
        for index, title_word_root in enumerate(doc['title_root']):

            for query_word_root in clean_query_root:
                if title_word_root == query_word_root:
                    title_match_value = title_match_value + doc['idf_word_list'][index]*normalization_factor

            for query_word_synonym_root in query_synonym_root:
                if title_word_root == query_word_synonym_root:
                    title_match_value = title_match_value + 0.75*doc['idf_word_list'][index]*normalization_factor

            for query_word_suggestion_root in query_suggestion_root:
                if title_word_root == query_word_suggestion_root:
                    title_match_value = title_match_value + 0.5*doc['idf_word_list'][index]*normalization_factor

        title_rank[doc['url']] = title_match_value


    title_unsorted_rank_dict={}

    for key, value in title_rank.items():
        if value>0:
            title_unsorted_rank_dict[key]=value


    return title_unsorted_rank_dict



