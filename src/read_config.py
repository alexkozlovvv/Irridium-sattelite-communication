#!/usr/bin/python

import yaml
import os


class Configfile(object):
    def __init__(self, config_path):
        self.config_path = config_path
        with open(os.sep.join([os.path.dirname(os.path.abspath(__file__)), self.config_path])) as config_file:
            self._config = yaml.load(config_file, Loader=yaml.FullLoader)
        self._working_directory = os.getcwd()

    def read_config(self):
        with open(os.sep.join([os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.config_path])) as config_file:
            self._config = yaml.load(config_file, Loader=yaml.FullLoader)
        return self._config

    def get_param(self, parameter):
        return self._config[parameter]
