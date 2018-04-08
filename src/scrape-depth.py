to_scrape = set()
to_scrape.add("/path-1")
to_scrape.add('/path-2')

# for i in list(scrape_items):

scraped_items = set() # uniqueness
scraped_items.add("/path-2")

def fetch_links_words(url):
    print(url, "scraping..")
    return set(["/path-3", "/path-4"]), ["words1", "words2"]

# , 
def scrape_links(to_scrape, scraped, current_depth=0, max_depth=3, words=[]):
    if current_depth <= max_depth:
        new_set_to_scrape = set() 
        while to_scrape:
            item = to_scrape.pop() 
            if item not in scraped:
                new_paths, new_words = fetch_links_words(item)
                words += new_words
                new_set_to_scrape = (new_set_to_scrape | new_paths) # removes extra
            scraped.add(item)
        current_depth += 1
        return scrape_links(new_set_to_scrape, scraped, current_depth=current_depth, max_depth=max_depth, words=words)
    return scraped, words


scraped, words = scrape_links(to_scrape, set(), current_depth=0, max_depth=3)
print(scraped, words)




