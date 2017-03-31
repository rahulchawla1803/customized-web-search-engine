from html.parser import HTMLParser
from urllib import request
from urllib import parse
from pymongo import MongoClient

client = MongoClient()
db=client.webSE
class LinkFinder(HTMLParser):


    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.tag_data = []
        self.tag_data_join = ""
        self.style_script_flag = 0
        self.title_data = ""
        self.title_flag=0;



    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for (attribute,value) in attrs:
                if attribute=='href':
                    #print("link is :"+value)
                    url=parse.urljoin(self.base_url, value)
                    self.links.add(url)
        elif tag=='title':
            self.title_flag=1;

        elif (tag=='script') or (tag=='style'):
            self.style_script_flag=1


    def handle_data(self, data):
        if (self.style_script_flag==0) and (self.title_flag==0) :
            self.tag_data.append(data)
        if self.title_flag==1:
            self.title_data=data
            #print("Title data is : "+data+"\n")

    def handle_endtag(self, tag):
        if tag=='html':
            self.tag_data_join=' '.join(self.tag_data)
            self.tag_data_join=" ".join((self.tag_data_join.split()))
            db.data.insert({"url":self.page_url,"title":self.title_data ,"content":self.tag_data_join})
        elif (tag == 'script') or (tag == 'style'):
            self.style_script_flag = 0
        elif tag=='title':
            self.title_flag=0

    def page_links(self):
        return self.links


                    #if the value is relative, base_url will be added else it'll be ignored, beauty of urljoin
# <sometimes instead of full url, sites have relative url thus they should be converted to full urls by adding base, home page url

    def error(self, message):
        pass

#finder=LinkFinder('https://thenewboston.com/','thenewboston.com')
#finder.feed('<html><title>Title1</title><head><a href="https://thenewboston.com/first">hsahahaha</a> <a href="/second">hsahahaha</a> <div><p> Hello, this is from the para</p> </div> </head></html>')
