import os
from stop_words import get_stop_words

# <Each website in separate folder, directory>

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating Folder '+ directory)
        os.makedirs(directory)


# <Creating queue and crawled files if not created>

def create_data_files(project_name, base_url):
    # <base_url from where the crawling starts>
    queue=project_name+'/queue.txt'
    crawled=project_name+'/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# <creating a new file>
def write_file(path, data):
    f=open(path,'w')
    f.write(data)
    f.close()

#create_data_files('thenewboston','https://thenewboston.com/')


def append_to_file(path, data):
    #'a' is for appending
    with open(path, 'a') as file:
        file.write(data+'\n')

# delete contents of a file
def delete_files_contents(path):
    with open(path, 'w'):
        pass


# read a file and convert each line to set items
'''
we work on sets rather than directly dealing with files as files are stored in memory
Thus file->set
'''
def file_to_set(file_name):
    results=set()
    with open(file_name,'rt') as f:
        #rt is reading text, equivalent to r as text is default
        for line in f:
            results.add(line.replace('\n',''))
    return results

# iterate through set and each value will be a newline in the file
def set_to_file(links, file):
    delete_files_contents(file)
    for link in sorted(links):
        append_to_file(file,link)


def cleaning(content):
    stop_words = get_stop_words('english')
    content = content.lower()
    content_clean = []
    temp = []
    words = content.split()
    for j in words:
        if j not in stop_words:
            temp.append(j)

    symbols = "!@#$%^&*(){}[]:;,\"'<>?./+_=.-|"
    for w in temp:
        for i in range(0, len(symbols)):
            w = w.replace(symbols[i], "")
        if len(w) > 0:
            content_clean.append(w)
    return content_clean




























