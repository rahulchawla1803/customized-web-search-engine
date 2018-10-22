from textblob import TextBlob

blob = TextBlob("Health.com: Fitness, Nutrition, Tools, News, Health Magazine")
print(blob.sentiment.polarity)