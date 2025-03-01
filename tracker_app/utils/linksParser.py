import typing
from urllib.parse import urlparse

def get_unique_domains(urls):
    return list({
        urlparse(url).netloc
        for url in urls
        if urlparse(url).netloc
    })