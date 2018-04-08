to_scrape = set()
to_scrape.add("/path-1")
to_scrape.add('/path-2')

# for i in list(scrape_items):

scraped_items = set() # uniqueness
scraped_items.add("/path-2")



# , 
def scrape_links(to_scrape, scraped, current_depth=0, max_depth=3):
    if current_depth <= max_depth:
        while to_scrape: # while items are in the set that equals true
            item = to_scrape.pop() # remove the item from the set
            if item not in scraped:
                print(item, "scrape these items") # this where i can scrape some more
                to_scrape.add("/path-1")
            scraped.add(item)
        current_depth += 1
        return scrape_links(to_scrape, scraped, current_depth=current_depth, max_depth=max_depth)
    return to_scrape, scraped


to_scrape, scraped = scrape_links(to_scrape, set(), current_depth=0, max_depth=3)
print(list(scraped))




