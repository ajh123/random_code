from typing import List
from models import Expression, Work
import requests
import xmltodict

works: List[Work] = []

api_token = "REDACTED"
api_url = 'https://legislation.minersonline.uk/api/v3/akn/zl/.json'


def call_url_with_token(url):
    resp = requests.get(url, headers={'Authorization': f'token {api_token}'})
    resp.raise_for_status()
    return resp

def handle():
    url = api_url

    # handle paginated results
    while url:
        resp = call_url_with_token(url).json()

        for result in resp.get('results', {}):
            create_work_and_expressions(result)

        url = resp['next']

def create_work_and_expressions(data):
    # for each result, create the Work object
    work = Work(data['frbr_uri'], data['title'], data)
    works.append(work)

    # for each work, create the relevant Expression objects
    for date in data['points_in_time']:
        for expression in date['expressions']:
            create_expression(expression, work)

def create_expression(data, work: Work):
    expression = Expression(
        work,
        data['expression_frbr_uri'],
        data['title'],
        data['language'],
        data['expression_date'],
        call_url_with_token(f"{data['url']}.xml").content.decode('utf-8'),
        call_url_with_token(f"{data['url']}/toc.json").json()
    )
    work.expressions.append(expression)

handle()
for work in works:
    print(f"== {work} ==")
    for expression in work.expressions:
        print(f"- {expression.date} ({expression.frbr_uri})")
        print(xmltodict.parse(expression.content))