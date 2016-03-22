# -*- coding: utf-8 -*-

import json
import requests

headers = {
    'Uuid': 'ios_5E37754C750F8F62B96A1AF59B3A9956',
    'Qbtoken': '831a7107707b0c6f593a66b79f5bf7100cee21b6',
    'Source': 'ios_8.2.15',
    'User-Agent': 'QiuBai/8.2.15 (iPhone; iPhone OS 9.1; zh_CN) PLHttpClient/1_WIFI'
}

data = {
    "district": "南山区",
    "content": "认为二位地方水电费水电费",
    "display": 1,
    "screen_width": 750,
    "longitude": 113.95718912947153,
    "screen_height": 1334,
    "anonymous": False,
    "latitude": 22.539976441023292,
    "city": "深圳市",
    "allow_comment": True
}

session = requests.Session()
files = {'json': ('', json.dumps(data))}
resp = session.post('http://m2.qiushibaike.com/article/create', files=files, headers=headers)
print resp.json()
