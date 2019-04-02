from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from urllib.parse import urlparse
import json
import csv

"""
    Helper functions
"""

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    #TODO replace by actual logs
    """
    print(e)

def get_hostname(long_url):
    r = urlparse(long_url)
    return r.hostname


def jdump(mydic):
    """ (JSON-Dump) Is a simple wrapper to savea a dictionary as JSON """
    title = mydic['title']
    file_name = f'{title}_info.json'
    with open(f'data/{file_name}', mode='w', encoding='utf-8') as fp:
        try:
            json.dump(mydic, fp, sort_keys=True, indent=4)
            print(f"Succes! '{title}' has been added to the recipe book.")
        except:
            print(f"Fail! Error adding '{title}' to the recipe book.")


def add_recipe_to_book(mydic):
    """ Adds recipe (dic) to recipe_book.csv """
    with open('data/recipe_book.csv', mode='a', newline='') as rb_file:
        fieldnames = ['title', 'ingredients', 'time_info', 'url']
        # fields
        title = mydic['title']
        # ing = mydic['ingredients']
        # timefo = mydic['time_info']
        # url = mydic['url']
        writer = csv.DictWriter(rb_file, fieldnames=fieldnames)
        try:
            writer.writerow({
                'title': mydic['title'],
                'ingredients': mydic['ingredients'],
                'time_info': mydic['time_info'],
                'url': mydic['url']})
            print(f"# Succes! '{title}' has been added to the recipe book.")
        except:
            print(f"# Fail! Could NOT add '{title}' to the recipe book.")


   