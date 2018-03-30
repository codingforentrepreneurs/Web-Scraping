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
    return requests.get(url)



def re_valid_url(url):
    http_regex = r'^https?://' # https or http
    pattern = re.compile(http_regex)
    is_a_match = pattern.match(url) # regex match or None
    if is_a_match is None:
        raise ValueError("This url does not start with http:// or https://")
    return url

def validate_url(url):
    url = re_valid_url(url)
    # if not "http" in url: # code.http.com
    #     raise ValueError("This is not a valid url")
    return url


def end_program():
    raise KeyboardInterrupt("Program forced to quit.")

def get_input():
    url = input("What is your url? ")
    if url == 'q':
        return end_program()
    try:
        validate_url(url)
    except ValueError as err:
        print(err)
        print("Type 'q' to quit lookup")
        return get_input()
    return url


def main():
    url = get_input()
    # call my url
    # parse
    # save

main()

