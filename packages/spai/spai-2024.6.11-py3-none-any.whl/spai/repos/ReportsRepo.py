import requests
import os

from .APIRepo import APIRepo


class ReportsRepo(APIRepo):
    def generate(self, body):
        return requests.post(self.url + "reports/generate", json=body, stream=True)
