import urllib.parse as url_prs

import json
import requests


def get_json(url):
    r = requests.get(url)
    return json.loads(r.content)


def quote_dict(d):
    return url_prs.quote(json.dumps(d))
