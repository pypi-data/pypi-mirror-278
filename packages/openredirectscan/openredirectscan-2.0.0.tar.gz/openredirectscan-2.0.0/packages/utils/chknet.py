import requests

def net():
    try:
        responce = requests.get("http://google.com",timeout=5)
        return True
    except(requests.ConnectionError,requests.Timeout):
        return False