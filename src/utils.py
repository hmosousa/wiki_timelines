import requests


def get_html(url: str) ->  str | None:
    if url is None:
        return None
        
    response = requests.get(url)
    if response.ok:
        return response.text
