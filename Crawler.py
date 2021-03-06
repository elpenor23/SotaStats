#!/usr/bin/python3
from ThreadedRunner import ThreadedRunner
import requests, time, sys, random, logging
from utils.utils import write_to_json_file, get_api_results, fileExists

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class Spider(ThreadedRunner):
    def initialize(self, args):
        """ initialize things we need to initialize """
        logging.basicConfig(filename='error.log', filemode='w', level=logging.WARNING)
        logging.warning("Start: Initializing...")

        all_association = get_api_results(self.config["associationAPIBase"])
        i = 0
        for association in all_association:
            if self.useThisAssociation(association, args):
                associationDetails = get_api_results(self.config["associationAPIBase"] + association["associationCode"])
                for region in associationDetails["regions"]:
                    regionDetails = get_api_results(self.config["regionAPIBase"] + region["associationCode"] + "/" + region["regionCode"] + "/")
                    for summit in regionDetails["summits"]:
                        if int(summit["activationCount"]) > 0 and not fileExists(self.config["dataLocationDirectory"] + region["associationCode"] + "/", self.create_file_name(summit["summitCode"])):
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
        self.completeInitialization()

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
        logging.basicConfig(filename='error.log',level=logging.WARNING)
        try:
            self.get_activations(data["association_code"], data["region_code"], data["summit_code"], str(data["summit_points"]), data["summit_name"])
        except Exception as ex:
            error_text = f"Getting Page Data Failed:{ex}Data: {data}"
            logging.warning(error_text)

        #after we are done update the progress bar
        self.completedTasks.append(data)
        self.updateStatus()

    def get_activations(self, association_code, region_code, summit_code, summit_points, summit_name):
        """ Getting directly from the API """
        data = get_api_results(self.config["summitAPIBase"] + summit_code)
        
        j = {
            "association_code": association_code,
            "region_code": region_code,
            "summit_code": summit_code,
            "summit_points": summit_points,
            "summit_name": summit_name,
            "activations": data
        }

        write_to_json_file(self.config["dataLocationDirectory"] + association_code + "/", self.create_file_name(summit_code), j)
    
    def create_file_name(self, summit_code):
        """ create the filename """
        return summit_code.replace("/", "-") + ".json"
