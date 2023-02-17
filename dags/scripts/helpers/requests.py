import requests
from requests.exceptions import Timeout, HTTPError, ConnectionError
from time import time

#Retorna el resultado o False en caso de no conseguirlo
def request_with_retry(request, MAX_RETRIES):
    for i in range(MAX_RETRIES):
        try:
            r = requests.get(request, timeout=100)
            r.raise_for_status()
            return r
        except ConnectionError as ce:
            print("Connection Error")
            return False
        except Timeout as tout:
            print(f"TimeOut Error, retrying ({i}/{MAX_RETRIES})")
        except HTTPError as err:
            print(r.status_code)
            if r.status_code == 429:
                print(r.content)
                time.sleep(int(r.headers["Retry-After"]) + 5)
            else:
                return False
    return False

#Retorna el resultado o False en caso de no conseguirlo
def post_request_with_retry(request, MAX_RETRIES, id):
    for i in range(MAX_RETRIES):
        try:
            r = requests.post(request, {"identifiers": id}, timeout=100)
            r.raise_for_status()
            return r
        except ConnectionError as ce:
            print("Connection Error")
            return False
        except Timeout as tout:
            print(f"TimeOut Error, retrying ({i}/{MAX_RETRIES})")
        except HTTPError as err:
            print(r.status_code)
            if r.status_code == 429:
                print(r.content)
                time.sleep(int(r.headers["Retry-After"]) + 5)
            else:
                return False
    return False