#!/usr/bin/python3
import os, logging
from ThreadedRunner import ThreadedRunner
from bs4 import BeautifulSoup
from utils.utils import translate_date, open_json_file
from utils.database import add_activation_record
from pathlib import Path

class Scraper(ThreadedRunner):
    def initialize(self, args):
        logging.basicConfig(filename='error.log', filemode='w', level=logging.WARNING)
        logging.warning("Start: Initializing...")

        if args[0] == "single":
            self.Q.append(args[1])
        else:
            self.Q = list(Path(self.config["dataLocationDirectory"]).rglob("*.json"))

        self.completeInitialization()

    def runner(self, work):
        try:
            json_data = open_json_file(work)

            for activation in json_data["activations"]:
                add_activation_record(activation["activationDate"], 
                                activation["ownCallsign"],
                                json_data["association_code"],
                                json_data["region_code"],
                                json_data["summit_code"], 
                                json_data["summit_name"], 
                                json_data["summit_points"], 
                                activation["qsos"])
        except Exception as ex:
            error_text = f"Getting Page Data Failed:{ex} Data: {work}"
            logging.warning(error_text)

        self.completedTasks.append(work)
        self.updateStatus()