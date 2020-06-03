import sys
import requests
from python_moonutilities import exceptions

def get(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise exceptions.ConsulError("request failure ",e)
    except:
        raise exceptions.ConsulError("Unexpected error ", sys.exc_info()[0])
    return response


def put(url, json=""):
    try:
        response = requests.put(url,json=json)
    except requests.exceptions.RequestException as e:
        raise exceptions.ConsulError("request failure ",e)
    except:
        raise exceptions.ConsulError("Unexpected error ", sys.exc_info()[0])
    return response