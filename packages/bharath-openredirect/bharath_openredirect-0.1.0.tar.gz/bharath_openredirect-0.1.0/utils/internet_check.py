# utils/internet_check.py

import requests

class InternetCheck:
    @staticmethod
    def check_connection(url='http://www.google.com/', timeout=5):
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except requests.RequestException:
            return False
