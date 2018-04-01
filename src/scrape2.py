import csv
import datetime
import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
from stop_words import get_stop_words

saved_domains = {
    "joincfe.com": {
        "tag": "div",
        "class": "main-container"
    },
    "tim.blog": {
        "tag": "div",
        "class": "content-area"
    },
}




def clean_word(word):
    word = word.replace("!", "") #.split()
    word = word.replace("?", "")
    word = word.replace(".", "")
    word = word.replace(":", "")
    word = word.replace(",", "")
    word = word.replace(";", "")
    word = word.replace(")", "")
    word = word.replace("(", "")
    word = word.replace("-", "")
    word = word.replace("--", "")
    word = word.replace('—', "")
    return word

def clean_up_words(words):
    new_words = [] # empty list
    pkg_stop_words = get_stop_words('en')
    my_stop_words = ['the', 'is', 'and', 'thisfacebooktwitteremailredditprint']
    for word in words:
        word = word.lower()
        cleaned_word = clean_word(word)
        if cleaned_word in my_stop_words or cleaned_word in pkg_stop_words:
            pass
        else:
            new_words.append(cleaned_word)
    return new_words

def fetch_url(url):
    '''
    Request package 1 time
    '''
    response = requests.Response()
    try:
        response = requests.get(url)
        #print(dir(response)) # python
        #print(response.__class__) # python
    except requests.exceptions.ConnectionError:
        print("Could not connect to the url. Please try again.")
    return response



def validate_url(url):
    http_regex = r'^https?://' # https or http # validate .co, .com, 
    pattern = re.compile(http_regex)
    is_a_match = pattern.match(url) # regex match or None
    if is_a_match is None:
        raise ValueError("This url does not start with http:// or https://")
    return url

def append_http(url):
    if not url.startswith("http"):
        return f'http://{url}'
    return url

def end_program():
    raise KeyboardInterrupt("Program forced to quit.")

def get_input():
    url = input("What is your url? ")
    if url == 'q':
        return end_program()
    url = append_http(url)
    try:
        validate_url(url)
    except ValueError as err:
        print(err)
        print("Type 'q' to quit lookup")
        return get_input()
    return url


def soupify(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_domain_name(url):
    return urlparse(url).netloc

def get_path_name(url):
    return urlparse(url).path

def get_url_lookup_class(url):
    domain_name = get_domain_name(url)
    lookup_class = {}
    if domain_name in saved_domains:
        '''
        change this to use a CSV file instead.
        '''
        lookup_class = saved_domains[domain_name]
    return lookup_class


def get_content_data(soup, url):
    lookup_dict = get_url_lookup_class(url)
    if lookup_dict is None:
        return soup.find("body").text
    return soup.find(lookup_dict['tag'], {"class": lookup_dict['class']})


def parse_links(soup):
    # <a href='/abc/'>Link</a>
    a_tags = soup.find_all("a", href=True)
    print(a_tags)
    links = []
    for a in a_tags:
        link = a['href'] # '/abc/', '/another/'
        links.append(link)
    return links

def get_local_paths(soup, url):
    links = parse_links(soup) # list of links
    local_paths = []
    domain_name = get_domain_name(url)
    for link in links:
        link_domain = get_domain_name(link) # <a href='http://yourodmain.com/some-local/-link/'>
        if link_domain == domain_name:
            path = get_path_name(link)
            local_paths.append(path)
        elif link.startswith("/"): # <a href='/some-local/-link/'>
            local_paths.append(link)
    return list(set(local_paths)) # removes duplicates and returns list

def main():
    url = get_input()
    response = fetch_url(url)
    if response.status_code not in range(200, 299): # Http Status Codes
        print(f"Invalid request, you cannot view this. {response.status_code}")
        return None
    response_html = response.text # html
    soup = soupify(response_html)
    html_soup = get_content_data(soup, url)
    #print(html_text)
    paths = get_local_paths(html_soup, url)
    print(paths)

    # call my url
    # parse
    # save

main()

