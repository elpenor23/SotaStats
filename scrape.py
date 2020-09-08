#!/usr/bin/python3
from Scraper import Scraper
from Crawler import Spider
import time

""" This will crawl the web and save the webpage for processing """
if __name__ == '__main__':
    start_time = time.time()

    print("Initializing Scraper")
    scraper = Scraper(["all"]) #["all", "W1-HA-159.json"])
    scraper.start()
    scraper.completeStatus()

    elapsed_time = time.time() - start_time

    print("Elapsed Time: " + str(elapsed_time))

    
