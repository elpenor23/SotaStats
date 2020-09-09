#!/usr/bin/python3
from Scraper import Scraper
import time

""" This will crawl the web and save the webpage for processing """
if __name__ == '__main__':
    start_time = time.time()

    print("Initializing Scraper")
    scraper = Scraper(["all"]) #["all", "W1-HA-159.json"])
    scraper.start()

    elapsed_time = time.time() - start_time

    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
