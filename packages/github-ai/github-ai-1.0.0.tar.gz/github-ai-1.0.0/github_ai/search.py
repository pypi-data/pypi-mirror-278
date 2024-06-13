import requests

def search_github_repositories(query, sort='stars', order='desc', per_page=None, page=None):
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

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
