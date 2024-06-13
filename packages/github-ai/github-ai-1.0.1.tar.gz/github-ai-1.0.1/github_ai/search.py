import requests
from requests.exceptions import HTTPError, Timeout, RequestException

def search(query, sort='stars', order='desc', per_page=None, page=None, timeout=10):
    url = "https://api.github.com/search/repositories"
    params = {
        'q': query + " is:public",
        'sort': sort,
        'order': order,
    }

    if per_page is not None:
        params['per_page'] = per_page
    if page is not None:
        params['page'] = page

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    except HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Timeout as timeout_err:
        raise Exception(f"Request timed out: {timeout_err}")
    except RequestException as req_err:
        raise Exception(f"Error during requests to {url}: {req_err}")
    except Exception as err:
        raise Exception(f"An error occurred: {err}")

def fix_query_issues(query):
    query = query.replace(' ', '+')
    return query

def fix_language_issues(language):
    language = language.replace(' ', '-')
    return language

def search_by_user(user, per_page=None, page=None):
    query = f"user : {user}"
    return search(fix_query_issues(query), per_page=per_page, page=page)

def search_by_language(language, per_page=None, page=None):
    query = f"language : {fix_language_issues(language)}"
    return search(fix_query_issues(query), per_page=per_page, page=page)

def search_by_topic(topic, per_page=None, page=None):
    query = f"topic : {fix_query_issues(topic)}"
    return search(fix_query_issues(query), per_page=per_page, page=page)
