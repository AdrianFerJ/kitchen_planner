from bs4 import BeautifulSoup
import helpers as hp
import json

# Import recipe specific scrappers
from recipe_scrappers import factory

def get_this_recipe(url):
    """
    Takes a recipe URL and returns key info (ingredients, time info, etc.)
    """
    print("# Starting scrapper...")
    print(f"# getting ingredients for '{url}'")

    # Get html content and prepare it for scrapping 
    raw_html = hp.simple_get(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Get hostname (i.e. 'www.allrecipes.com')
    hostname = hp.get_hostname(url)

    # Get a scrapper that matches hostname and pass url+soup for scrapping
    scrapper = factory.get_scrapper(hostname)
    recipe_info = scrapper(url, soup)

    if recipe_info:
        print("# Recipe scrapped!")
        pretty_data = json.dumps(recipe_info, indent=4)
        print(pretty_data)
        hp.add_recipe_to_book(recipe_info)
    else:
        print("Error!")


"""
    Run Script
"""

if __name__ == '__main__':
    # Recipe url (Feel free to change the test URL)
    TEST_URL = 'https://www.allrecipes.com/recipe/257938/spicy-thai-basil-chicken-pad-krapow-gai/?clickId=right%20rail1&internalSource=rr_feed_recipe_sb&referringId=60598%20referringContentType%3Drecipe'
    #'https://www.allrecipes.com/recipe/60598/vegetarian-korma/?internalSource=hub%20recipe&referringContentType=Search'

    # Request recipe! 
    get_this_recipe(TEST_URL)