# includes/scanning.py

import requests
from urllib.parse import urljoin
class Scanning:
    def __init__(self, urls=None, payloads=None):
        self.urls = urls if urls else []
        self.payloads = payloads if payloads else []
    def add_url(self, url):
        self.urls.append(url)
    def add_payloads_from_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.payloads = [line.strip() for line in file.readlines()]
        except Exception as e:
            print(f"Error reading payloads from file {file_path}: {e}")
    def is_url_alive(self, url):
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Error checking URL {url}: {e}")
            return False
    def brute_force_single_payload(self, payload):
        for url in self.urls:
            test_url = urljoin(url, payload)
            try:
                response = requests.get(test_url, allow_redirects=False)
                if 'Location' in response.headers:
                    location = response.headers['Location']
                    if location.startswith(payload):
                        print(f"Potential open redirect detected: {test_url} redirects to {location}")
                    else:
                        print(f"No open redirect detected for {test_url}")
                else:
                    print(f"No redirection header for {test_url}")
            except requests.RequestException as e:
                print(f"Error checking for open redirect on {test_url}: {e}")
    def start_scan(self):
        for url in self.urls:
            if self.is_url_alive(url):
                print(f"URL is alive: {url}")
                for payload in self.payloads:
                    self.brute_force_single_payload(payload)
            else:
                print(f"URL is not alive: {url}")
