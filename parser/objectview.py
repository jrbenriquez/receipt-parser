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


class ObjectView(object):
    """ View objects as dicts """

    def __init__(self, d):
        """
        :param d: {}
            Object data
        """

        self.__dict__ = d

    def get(self, key, default_value=None):
        if hasattr(self.__dict__, key):
            return self.__dict__[key]
        else:
            return default_value
