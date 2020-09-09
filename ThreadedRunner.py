#!/usr/bin/python3
import threading
from utils.utils import open_json_file
from concurrent.futures import ThreadPoolExecutor

class ThreadedRunner():
    """ Sets up the up the UI """
    def __init__(self, args):
        """ setup required things """
        self.config = self.config = open_json_file("config/config.json")
        self.Q = []
        self.completedTasks = []
        self.threads = []
        self.initialize(args)

    def initialize(self, args):
        """ initialize things we need to initialize """
        print("ERROR: initialize must be overridden!")
        raise Exception('Inheritance Error', 'initialize must be overridden')

    def runner(self, data):
        """ worker to do the things """
        print("ERROR: runner must be overridden!")
        raise Exception('Inheritance Error', 'runner must be overridden')

    def start(self):
        self.updateStatus(0)
        with ThreadPoolExecutor(max_workers=self.config["numberOfThreads"]) as executor:
            for work in self.Q:
                self.threads.append(executor.submit(self.runner, work))

        self.completeStatus(str(len(self.completedTasks)) + " Tasks have been completed!")
        
    def completeInitialization():
        self.updateStatus(100, 100)
        self.completeStatus("Initilization Complete")
        print(str(len(self.Q)) + " items added to the Queue.")

    def updateStatus(self, current = 0, total = 0):
        if total == 0:
            total = len(self.Q)
        if current == 0:
            current = len(self.completedTasks)

        fill = '█'
        decimals = 1
        prefix = 'Progress:'
        suffix = 'Complete'
        length = 50
        printEnd = "\r"

        percent = ("{0:." + str(decimals) + "f}").format(100 * (current / float(total)))
        filledLength = int(length * current // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

    def completeStatus(self, message = None):
        print()
        if message is not None:
            print(message)
