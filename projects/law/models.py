from typing import List
from datetime import datetime


class Work:
    def __init__(self, frbr_uri: str, title: str, metadata: str):
        self.frbr_uri = frbr_uri
        self.title = title
        self.metadata = metadata
        self.expressions: List['Expression'] = []

    def __str__(self):
        return f'{self.title} ({self.frbr_uri})'


class Expression:
    def __init__(self, work: Work, frbr_uri: str, title: str, language_code: str, date: datetime, content: str, toc_json):
        self.work = work
        self.frbr_uri = frbr_uri
        self.title = title
        self.language_code = language_code
        self.date = date
        self.content = content
        self.toc_json = toc_json

    class Meta:
        # latest first
        ordering = ['-date']

    def __str__(self):
        return f'{self.title} ({self.frbr_uri})'
