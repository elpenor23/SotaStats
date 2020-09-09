#!/usr/bin/python3
from Crawler import Spider
import time

""" This will crawl the web and save the webpage for processing """
if __name__ == '__main__':
    start_time = time.time()

    print("Initizing Spider")
    spider = Spider(["code", "W6"]) #W1, W0C
    print("Crawling")
    spider.start()

    elapsed_time = time.time() - start_time

    print("Elapsed Time: " + str(elapsed_time))
