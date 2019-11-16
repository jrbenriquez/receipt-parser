
# !/usr/bin/python3
# coding: utf-8

# Copyright 2015-2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import dateutil.parser
import re
from difflib import get_close_matches

from parser.objectview import ObjectView

class Receipt(object):
    """ Market receipt to be parsed """

    def __init__(self, config, raw):
        """
        :param config: ObjectView
            Config object
        :param raw: [] of str
            Lines in file
        """

        self.config = config
        self.market = self.date = self.sum = None
        self.lines = raw
        self.normalize()
        self.parse()

    def normalize(self):
        """
        :return: void
            1) strip empty lines
            2) convert to lowercase
            3) encoding?

        """

        self.lines = [
            line.lower() for line in self.lines if line.strip()
        ]

    def parse(self):
        """
        :return: void
            Parses obj data
        """

        self.market = self.parse_market()
        self.date = self.parse_date()
        self.sum = self.parse_sum()

    def fuzzy_find(self, keyword, accuracy=0.6):
        """
        :param keyword: str
            The keyword string to look for
        :param accuracy: float
            Required accuracy for a match of a string with the keyword
        :return: str
            Returns the first line in lines that contains a keyword.
            It runs a fuzzy match if 0 < accuracy < 1.0
        """

        for line in self.lines:
            words = line.split()
            # Get the single best match in line
            matches = get_close_matches(keyword, words, 1, accuracy)
            if matches:
                return line

    def parse_date(self):
        """
        :return: date
            Parses data
        """
        date_str = None
        for line in self.lines:
            m = re.search(self.config['date_format1'], line) # Base Regex that almost catches all date
            if m:  # We"re happy with the first match for now
                # validate date using the dateutil library (https://dateutil.readthedocs.io/)
                date_str = m.group(1)
            else:
                #TODO loop through the available regex for date for matches
                m = re.search(self.config['date_format2'], line) # Let's use a backup regex just to be sure we are not missing anything
                # validate date using the dateutil library (https://dateutil.readthedocs.io/)
                if m:
                    date_str = m.group(1)
            if date_str and hasattr(m,'groups') and '' not in m.groups(): # Make sure no groups is null since this is a date
                try:
                    dateutil.parser.parse(date_str)
                    return date_str
                except Exception as e:
                    # Not Valid string proceed with next
                    str(e).replace(',', '')

    def parse_market(self):
        """
        :return: str
            Parses market data
        """

        for int_accuracy in range(10, 6, -1):
            accuracy = int_accuracy / 10.0

            for market, spellings in self.config['markets'].items():
                for spelling in spellings:
                    line = self.fuzzy_find(spelling, accuracy)
                    if line:
                        print(line, accuracy, market)
                        return market

    def parse_sum(self):
        """
        :return: str
            Parses sum data
        """

        for sum_key in self.config['sum_keys']:
            sum_line = self.fuzzy_find(sum_key)
            if sum_line:
                # Replace all commas with a dot to make
                # finding and parsing the sum easier
                sum_line = sum_line.replace(",", ".")
                # Parse the sum
                sum_amount = re.search(self.config['sum_format'], sum_line)
                if sum_amount:
                    total_detected = sum_amount.group(0).replace(' ', '')
                    cleaned_total = re.sub('[^a-zA-Z0-9 \n\.]', '.', total_detected)
                    return cleaned_total
