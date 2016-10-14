#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sci-Hub PDF downloader through Tor Network
# Copyright (C) 2016 Rodrigo Martínez <dev@brunneis.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from TorCtl import TorCtl
import urllib2
import urllib
import requests
import sys
from bs4 import BeautifulSoup
import magic
import os

# Headers
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
headers={'User-Agent':user_agent}

# Proxy handler
proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})

def tor_get(url):
    # Opener instance
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)

    # Request
    request = urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()

def tor_post(url, data):
    # Request type
    method = 'POST'

    # Opener instance
    opener = urllib2.build_opener(proxy_support)

    # Request
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(url, data=encoded_data)
    request.add_header("Content-Type",'application/x-www-form-urlencoded')

    # Overwrite get method
    request.get_method = lambda: method

    try:
        connection = opener.open(request)
    except urllib2.HTTPError, ex:
        connection = ex

    if connection.code == 200:
       return connection.read()
    else:
        return -1

# URL
url = 'http://scihub22266oqcxt.onion/'

# Query
if len(sys.argv) < 2:
	print "The DOI parameter is missing."
	sys.exit()
	
# DOI argument
query = sys.argv[1]

response = tor_post(url, {'request': query})
if response == -1:
    print "Error processing the request."
    sys.exit()

html = BeautifulSoup(response, 'html.parser')
file_iframe = html.find('iframe', id='pdf')
if not hasattr(file_iframe, 'src'):
    print "Error retrieving the file (may not be available)."
    sys.exit()

# File write
file_path = '/data/' + query.replace('/', '_').replace(' ', '_') + '.pdf'
f = open(file_path, 'wb')
f.write(tor_get(file_iframe['src']))
f.close()

if magic.from_file(file_path, mime=True) != 'application/pdf':    
    print "Error retrieving the file (captcha?). Please, try again."
    os.remove(file_path)