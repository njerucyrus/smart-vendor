import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class RequestSession:
    def __init__(self):
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self.session = session
