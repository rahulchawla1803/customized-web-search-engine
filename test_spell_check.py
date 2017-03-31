import enchant

dict = enchant.Dict("en_UK")
print(dict.check('kh'))
'''
length_clean_query=len(clean_query)

for word in clean_query[:length_clean_query+1]:
    if dict.check(word) is False:
        suggestions=dict.suggest(word)
        for i in suggestions:
            clean_query.append(i)

print(search_query)
'''