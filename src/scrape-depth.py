to_scrape = set()
to_scrape.add("/path-1")
to_scrape.add('/path-2')

# for i in list(scrape_items):

scraped_items = set()
scraped_items.add("/path-2")

while to_scrape: # while items are in the set that equals true
    item = to_scrape.pop() # remove the item from the set
    if item not in scraped_items:
        print(item, "scrape these items") # this where i can scrape some more
    scraped_items.add(item)
