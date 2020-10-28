'''
'''
import os
from art_spider import ArtSpider
from scrapy.crawler import CrawlerProcess

class SpiderSpeaker:
    def __init__(self, last_page_scraped=0):
        self.last_page_scraped = last_page_scraped

    def scrape_page(self, page_txt):
        '''Reads the previously scraped page (stored in page.txt) and runs the spider on a new
        page. Rewrites the new page number in page.txt and updates last_page_scraped
        '''
        # Read the last page scraped in page.txt
        page_to_scrape = 0
        page = open(page_txt, 'r')
        value = page.read()
        # If no value has been stored yet, set page_to_scrape to 1
        if not value:
            page_to_scrape = 1
        # If a value has been stored, add 1 to it
        else:
            page_to_scrape = int(value) + 1
        page.close()
        
        print('Scraping page #%s' % page_to_scrape)
        
        # Have the spider scrape the current page
        process = CrawlerProcess()
        process.crawl(ArtSpider, page = page_to_scrape)
        process.start()
        
        # Update the last_page_scraped
        self.last_page_scraped = page_to_scrape
        
        page = open(page_txt, 'w')
        page.write(str(self.last_page_scraped))
        page.close()
        
        # Print confirmation
        print('Scraped page #%s' % self.last_page_scraped) 
    
