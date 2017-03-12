from urllib.parse import urlparse


# Get domain name(example.com)
def get_domain_name(url):
    try:
        results=get_host_name(url).split('.')
        return results[-2] + '.' +results[-1]
    except:
        return ''

# Get host name (mail.example.com) OR (gov.ind.xyz.example.com)
def get_host_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
