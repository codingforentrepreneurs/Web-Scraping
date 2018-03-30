import csv
import datetime
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
from stop_words import get_stop_words
# print("Hello world\"")
# my_url = "http://joincfe.com/blog/"

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

def create_csv_path(csv_path):
    if not os.path.exists(csv_path):
        with open(csv_path, 'w') as csvfile: # open that path w = write/create
            header_columns = ['word', 'count', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=header_columns)
            writer.writeheader()

saved_domains = {
    "joincfe.com": "main-container",
    "tim.blog": "content-area"
}

my_url = input("Enter the url to scrape: ") 

print("Grabbing...", my_url)
domain = urlparse(my_url).netloc # domain name
print("via domain", domain)

response = requests.get(my_url) # go to the url and get it
print("Status is", response.status_code) # 200, 403, 404, 500, 503

if response.status_code != 200: # not equal, == equal
    print("You can't scrape this", response.status_code)
else:
    print("Scraping..")
    # print(response.text)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    if domain in saved_domains:
        div_class = saved_domains[domain]
        body_ = soup.find("div", {"class": div_class})
    else:
        body_ = soup.find("body")
    #print(body_.text)
    words = body_.text.split() # removing stop words
    clean_words = clean_up_words(words)
    word_counts = Counter(clean_words)
    print(word_counts.most_common(30))
    filename = domain.replace(".", "-") + '.csv' # tim.blog, joincfe.com    
    path  = 'csv/' + filename # os.path
    timestamp = datetime.datetime.now() # timestamp
    create_csv_path(path)
    with open(path, 'a') as csvfile: # open that path w = write/create
        header_columns = ['word', 'count', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=header_columns)
        for word, count in word_counts.most_common(30):
            writer.writerow({
                    "count": count,
                    "word": word,
                    "timestamp": timestamp
                })




