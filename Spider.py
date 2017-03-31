from urllib.request import urlopen
from link_finder import LinkFinder
from general import *

#general is general.py
#the whole project starts from boot() execution, then it will create directory->queue,crawled files...
'''
will crawl a webpage, pass all the new links encountered to the queue and put this webpage's link from queue to crawled
'''
class spider:
    #<defining class variables(SHARED VARIABLES), shared among all instances, that is it's value can be changed by any instance(object) of the class >
    project_name=''
    base_url=''
    domain_name=''
    queue_file=''
    crawled_file=''
    queue=set()
    crawled=set()

    def __init__(self, project_name, base_url, domain_name):
        spider.project_name=project_name
        #it is spider. and not self. as the variables are shared variables
        spider.base_url=base_url
        spider.domain_name=domain_name
        spider.queue_file=spider.project_name+'/queue.txt'
        spider.crawled_file = spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First Spider',spider.base_url)


    '''
    # boot method need not be in the class spider as it is only using class(shared) variables and
     not instance variable(specific to an instance) but still be put in class spider thus as coding convention
     we add @staticmethod
    '''

    @staticmethod
    def boot():
        create_project_dir(spider.project_name)
        create_data_files(spider.project_name, spider.base_url)
        spider.queue=file_to_set(spider.queue_file)
        spider.crawled=file_to_set(spider.crawled_file)




    @staticmethod
    def crawl_page(thread_name, page_url):


        if page_url not in spider.crawled:
            print(thread_name + ' now crawling '+page_url)
            print('queue '+str(len(spider.queue))+' || '+' crawled '+str(len(spider.crawled)))
            spider.add_links_to_queue(spider.gather_links(page_url))
            spider.queue.remove(page_url)
            spider.crawled.add(page_url)
            print("page just crawled : "+page_url)
            spider.update_files()


    '''
    when we use urllib.request urlopen to get the HTML page it is returned in byte format and not in string and
    class LinkFinder in link_finder.py handles HTML page in string format
    '''

    @staticmethod
    def gather_links(page_url):
        html_string=''
        try:
            response=urlopen(page_url)
            #res_get_head=response.getheader("Content-Type")
            #print("Response.getheader type = "+res_get_head)
            if 'text/html' in response.getheader("Content-Type"):
                html_bytes=response.read()
                html_string=html_bytes.decode('utf-8')
                finder=LinkFinder(spider.base_url,page_url)
                finder.feed(html_string)

        except (RuntimeError, TypeError, NameError):
            print("Page url : "+ page_url)
            print("Error: can not crawl the page\n")
            print(RuntimeError+"\n"+TypeError+"\n"+NameError)
            return set()
            #that is returning empty set so that the whole project doesn't crash off and starts with the next queued link

        return finder.page_links()


    @staticmethod
    def add_links_to_queue(links):
        #print(links)
        for url in links:
            if url in spider.queue:
                continue
            if url in spider.crawled:
                continue
            if url[0:26] !='http://www.health.com/food':
                continue
            if spider.domain_name not in url:
                continue
            if url[-4:] == '.pdf' or url[-4:] =='.jpg':
                continue
            if url[-4:] == '.xls' or url[-4:] =='.doc':
                continue
            if url[-5:] == '.xlsx':
                continue
            if "mailto:" in url:
                continue
            spider.queue.add(url)

        #print("hello:")
        #print(spider.queue)

    @staticmethod
    def update_files():
        set_to_file(spider.queue,spider.queue_file)
        set_to_file(spider.crawled,spider.crawled_file)










































