import threading
from queue import Queue
from Spider import spider
from domain import *
from general import *

#PROJECT_NAME='thenewboston'
PROJECT_NAME='health_food'
#PROJECT_NAME='rvce'

#HOMEPAGE='https://thenewboston.com/'
HOMEPAGE='http://www.health.com/food/'
#HOMEPAGE='http://rvce.edu.in/'

#DOMAIN_NAME=get_domain_name(HOMEPAGE)
DOMAIN_NAME='health.com/food'



QUEUE_FILE=PROJECT_NAME + '/queue.txt'
CRAWLED_FILE=PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS=50

# queue variable is basically thread queue
queue=Queue()
spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


#create worker threads (die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        # daemon so that thread dies when main exits
        t.start()
        # with t.start() thread will start executing the target, that is the work function, initially queue is empty so it will wait

# do the next job in the queue
def work():
    while True:
        url=queue.get()
        spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()




# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


#str(len(set)) will give number of elements in the set and convert it into string

#check if there are item in queue, and crawl them

def crawl():
    queue_links=file_to_set(QUEUE_FILE)
    if (len(queue_links)) > 0:
        print(str(len(queue_links))+ ' links in the queue')
        create_jobs()

'''
READ queue.get(block=True, timeout=None)
Initially threads are created and they are assigned to execute function "work()".
In work(), queue.get() initially will be empty thus it will block that thread for timeout=None(that is unlimited time till queue has an element)
Meanwhile crawl() will create_jobs() and as soon as the queue has element, the thread will start executing work()
'''

create_workers()
crawl()

