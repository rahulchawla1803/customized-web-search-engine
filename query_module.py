import json
from general import cleaning
import enchant
from stemming.porter2 import stem

dictionary_spelling = enchant.Dict("en_UK")

def query_structure(search_query):

    query_synonym = []
    query_suggestion = []
    word_synonyms = []
    word_suggestions=[]

    synonym_docs=[]
    for line in open('synonym.json', 'r'):
        synonym_docs.append(json.loads(line))


    print(search_query)
    clean_query = cleaning(search_query)

    for word in clean_query:
        for doc in synonym_docs:
            if word in doc['words']:
                query_synonym = query_synonym + doc['words']

    print(query_synonym)


    for word in clean_query:
        word_suggestions = dictionary_spelling.suggest(word)
        query_suggestion = query_suggestion+word_suggestions


    clean_query_root = []
    for word in clean_query:
        root_word = stem(word)
        clean_query_root.append(root_word)

    query_synonym_root = []
    for word in query_synonym:
        root_word = stem(word)
        query_synonym_root.append(root_word)


    query_suggestion_root = []
    for word in query_suggestion:
        root_word = stem(word)
        query_suggestion_root.append(root_word)

    return clean_query_root, query_synonym_root, query_suggestion_root