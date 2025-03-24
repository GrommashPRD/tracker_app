from typing import List
from urllib.parse import urlparse

def get_unique_domains(urls: List[str]) -> List[str]:
    return list({
        urlparse(url).netloc
        for url in urls
        if urlparse(url).netloc
    })