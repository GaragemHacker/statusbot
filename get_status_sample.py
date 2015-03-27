#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#Sample how to get hackerspace status with python

import urllib

status = urllib.urlopen('http://garagemhacker.org/status.txt').read()

print status