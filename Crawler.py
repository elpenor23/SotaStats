#!/usr/bin/python3
from ThreadedRunner import ThreadedRunner
import requests, time, sys, random
from utils.utils import write_to_json_file, get_api_results

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class Spider(ThreadedRunner):
    def initialize(self, args):
        """ initialize things we need to initialize """
        all_association = get_api_results(self.config["associationAPIBase"])
        i = 0
        for association in all_association:
            if self.useThisAssociation(association, args):
                associationDetails = get_api_results(self.config["associationAPIBase"] + association["associationCode"])
                for region in associationDetails["regions"]:
                    regionDetails = get_api_results(self.config["regionAPIBase"] + region["associationCode"] + "/" + region["regionCode"] + "/")
                    for summit in regionDetails["summits"]:
                        if int(summit["activationCount"]) > 0:
                            if i < 100:
                                i += 1
                            else:
                                i = 0
                            self.updateStatus(i, 100)
                            summit_data = {
                                "association_code": region["associationCode"], 
                                "region_code": region["regionCode"], 
                                "summit_code": summit["summitCode"], 
                                "summit_points": summit["points"], 
                                "summit_name": summit["name"]
                            }
                            
                            self.Q.append(summit_data)
        self.updateStatus(100, 100)
        self.completeStatus("Initilization Complete")
        print(str(len(self.Q)) + " summits added to the Queue.")

    def useThisAssociation(self, association, args):
        """ to filter which associations we check """
        if len(args) < 2:
            return True

        if args[0] == "name":
            return args[1] in association["associationName"]
        elif args[0] == "code":
            return args[1] == association["associationCode"]
        else:
            return True

    def runner(self, data):
        """ worker to do the things """
        self.get_page(data["association_code"], data["region_code"], data["summit_code"], str(data["summit_points"]), data["summit_name"])

        #after we are done update the progress bar
        self.completedTasks.append(data)
        self.updateStatus()

    def get_page(self, association_code, region_code, summit_code, summit_points, summit_name):
        """ scrape the html and save it locally for processing """
        URL = self.config["summitPageBase"] + summit_code

        if URL is None:
            print("Bad URL!: " + str(URL))

        #setup the browser headless
        opts = Options()
        opts.headless = True
        browser = Firefox(executable_path='/usr/bin/geckodriver', options=opts)
        
        #get the webpage
        browser.get(URL)

        #wait to make sure that the angular app loads
        wait = WebDriverWait(browser, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ng-star-inserted")))

        #get the page and close the browser
        html = browser.page_source

        browser.close()

        j = {
            "association_code": association_code,
            "region_code": region_code,
            "summit_code": summit_code,
            "summit_points": summit_points,
            "summit_name": summit_name,
            "webpage": html
        }

        write_to_json_file(self.config["dataLocationDirectory"], summit_code.replace("/", "-") + ".json", j)