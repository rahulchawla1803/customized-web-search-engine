from nltk.corpus import wordnet

dog = wordnet.synset("color.n.01")
print(dog.lemma_names())
