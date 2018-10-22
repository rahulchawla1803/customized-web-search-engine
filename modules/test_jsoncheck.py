import json

docs = []
for line in open('synonym.json', 'r'):
    docs.append(json.loads(line))

print(docs[0]['words'])

'''
fr=open('synonym.json', 'r', encoding="utf8")
data=fr.read()
print(data)
'''