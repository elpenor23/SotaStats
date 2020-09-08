#!/usr/bin/python3
import os
from ThreadedRunner import ThreadedRunner
from bs4 import BeautifulSoup
from utils.utils import translate_date, open_json_file
from utils.database import add_activation_record

class Scraper(ThreadedRunner):
    def initialize(self, args):
        print("Initializing Scraper")
        if args[0] == "single":
            self.Q.append(args[1])
        else:
            self.Q = os.listdir(self.config["dataLocationDirectory"])

        self.updateStatus(1,1)
        self.completeStatus("Intializing Complete")
        print(str(len(self.Q)) + " items added to the Queue.")

    def runner(self, work):
        json_data = open_json_file(self.config["dataLocationDirectory"] + work)

        data = self.scrape_html(str(json_data["webpage"]))

        for activation in data["activations"]:
            add_activation_record(activation["activation_date"], 
                            activation["activation_callsign"],
                            json_data["association_code"],
                            json_data["region_code"],
                            json_data["summit_code"], 
                            json_data["summit_name"], 
                            json_data["summit_points"], 
                            activation["activation_number_of_qso"])
        self.completedTasks.append(work)
        self.updateStatus()

    def scrape_html(self, html):
        """ process page """
        #time to parse the page and get the data
        soup = BeautifulSoup(html, "html.parser")

        app = soup.find("app-data-table")

        data = {
            "activations":[]
        }

        if app is None:
            return data

        table = app.find("tbody").findAll("tr")

        for tr in table:
            # print("new activation")
            tds = tr.findAll("td")
            # print(tds[0].text, tds[1].text, tds[2].text)
            activation = {}
            activation["activation_date"] = translate_date(tds[0].text.strip())
            activation["activation_callsign"] = tds[1].text.strip()
            activation["activation_number_of_qso"] = int(tds[2].text.strip())
            data["activations"].append(activation)

        return data
