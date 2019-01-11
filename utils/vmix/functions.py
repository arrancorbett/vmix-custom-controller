import requests
from urllib.parse import urlparse, parse_qs

def runScheduleTask(name, url, watevs, id):
    url = 'http://' + url

    o = urlparse(url)
    query = parse_qs(o.query)
    url = o._replace(query=None).geturl()

    response = requests.request("POST", url, headers={'Content-Type': "application/x-www-form-urlencoded"}, params=query)

    if response.text == 'Function completed successfully.':
        return True


class function:
    def __init__(self, name, type):
        self.name = name
        self.age = type
