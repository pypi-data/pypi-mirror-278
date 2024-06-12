# web_monitor/checker.py
import requests
import re
import logging

class WebsiteChecker:
    def __init__(self, url, regex=None):
        self.url = url
        self.regex = regex

    def check(self):
        try:
            response = requests.get(self.url, timeout=5)
            response_time = response.elapsed.total_seconds()
            status_code = response.status_code
            content_match = bool(re.search(self.regex, response.text)) if self.regex else None
            return {
                'url': self.url,
                'response_time': response_time,
                'status_code': status_code,
                'content_match': content_match
            }
        except requests.RequestException as e:
            logging.error(f"Error checking {self.url}: {e}")
            return {
                'url': self.url,
                'response_time': None,
                'status_code': None,
                'content_match': None,
                'error': str(e)
            }
