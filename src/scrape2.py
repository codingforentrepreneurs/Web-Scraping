import csv
import datetime
import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
from stop_words import get_stop_words

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


def main():
    url = get_input()
    response = fetch_url(url)
    if response.status_code not in range(200, 299): # Http Status Codes
        print(f"Invalid request, you cannot view this. {response.status_code}")
        return None
    response_html = response.text # html
    soup = soupify(response_html)



    # call my url
    # parse
    # save

main()

