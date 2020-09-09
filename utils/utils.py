#!/usr/bin/python3
import json
from datetime import date
import os
import requests
from requests.exceptions import HTTPError
import logging

def open_json_file(filename):
    """ Opens the passed in JSON file read only and returns it as a python dictionary"""
    try:
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
    except IOError:
        error_text = "Could not read config file: " + filename
        print(error_text)
    else:
        return json_data

def write_to_json_file(dir, file_name, data):
    """ writes the passed in json string to the passed in filename """
    logging.basicConfig(filename='error.log',level=logging.WARNING)
    try:
        if not os.path.isdir(dir):
            os.mkdir(dir)

        with open(dir + file_name, "w") as data_file:
            json.dump(data, data_file)
    except Exception as ex:
        error_text = f"Error Could not write to file:{ex}"
        logging.warning(error_text)

def fileExists(dir, file_name):
    """ checks if a file exists """
    return os.path.isfile(dir + file_name)

def get_api_results(api_url):
    """attempts to get results passed back from the passed in API"""
    logging.basicConfig(filename='error.log',level=logging.WARNING)

    json_results = ""

    try:
        request = requests.get(api_url)
        json_results = json.loads(request.text)
    except HTTPError as http_err:
        error_text = f"HTTP Error Could not get weather:{http_err}"
        logging.warning(error_text)
    except ConnectionError as http_con_err:
        error_text = f"HTTP Connection Pool Error Could not get weather:{http_con_err}"
        logging.warning(error_text)
    except json.JSONDecodeError as err:
        error_text = f'JSON Decoding error occurred: {err} Data: {request}'
        logging.warning(error_text)
    except Exception as err:
        error_text = f'Unknown error occurred: {err}'
        logging.warning(error_text)

    return json_results

def translate_date(raw_date):
    """ translates weird date format to a real datetime object """
    date_parts = raw_date.split()
    final_date = date(int(date_parts[2].strip()), int(translate_month(date_parts[1].strip())), int(date_parts[0].strip()))
    return final_date

def translate_month(month_text):
    """ translates month name to number """
    if month_text == "Jan":
        return 1
    elif month_text == "Feb":
        return 2
    elif month_text == "Mar":
        return 3
    elif month_text == "Apr":
        return 4
    elif month_text == "May":
        return 5
    elif month_text == "Jun":
        return 6
    elif month_text == "Jul":
        return 7
    elif month_text == "Aug":
        return 8
    elif month_text == "Sep":
        return 9
    elif month_text == "Oct":
        return 10
    elif month_text == "Nov":
        return 11
    elif month_text == "Dec":
        return 12
