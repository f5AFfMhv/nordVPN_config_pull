#!/usr/bin/env python

"""
This script is for pulling all nordVPN servers config files from their website (as it is in 2019 april).


Copyright (C) 2019 Martynas J. 
f5AFfMhv@protonmail.com  
https://github.com/f5AFfMhv

This file is part of nordVPN_config_pull.

    nordVPN_config_pull is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    nordVPN_config_pull is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with nordVPN_config_pull.  If not, see <https://www.gnu.org/licenses/>.
"""

# TODO:
# FIXME:

import urllib2 # Library for interacting with websites
import re # Regular expression library
from collections import defaultdict 

# NordVPN urls
listBaseUrl = "https://nordvpn.com/ovpn/"
configBaseUrl = "https://downloads.nordcdn.com/configs/files/ovpn_legacy/servers/"

def pull_servers():
    # Choose tcp or udp servers you want
    protocol = raw_input('What protocol servers you want to download? (udp is recomended) [tcp/udp]: \n')
    if protocol != "udp" and protocol != "tcp":
        print "Bad protocol: " + protocol + ". Only udp and tcp is viable options."
    else:
        # Download html of listBaseUrl
        configFileList = defaultdict(list)
        req = urllib2.Request(listBaseUrl, headers={'User-Agent' : "Magic Browser"}) 
        try:
            con = urllib2.urlopen(req)
            listHtml = con.read()
        except:
            print "Error opening " + listBaseUrl
            return
        # Get each config file download link from html
        index = 0
        for configFile in listHtml.split():
            if re.search(".nordvpn.com." + protocol, configFile):
                configFileList[index] = re.sub(r'^' + re.escape('href='), '', configFile).replace('"', "")
                index +=1 
        if index == 0:
            print "No servers found. It's possible nordVPN changed something again and this method for downloading config files doesn't work anymore"
        else:
            # Start downloading server config files
            print "Found " + str(index) + " servers to download"
            question = raw_input('Start downloading to servers directory? [y/n] \n')
            if question == "y":
                for i in xrange(0, index):
                    try:
                        url = str(configFileList[i])
                        name = re.sub(r'^' + re.escape(configBaseUrl), '', url)
                        print name + " \t\t[" + str(i) + "/" + str(index) + "]"
                        response = urllib2.urlopen(url)
                        data = response.read()
                        file_ = open("./servers/" + name, 'w')
                        file_.write(data)
                        file_.close()
                    except:
                        print "Can't download file" + " \t\t[" + str(i) + "/" + str(index) + "]"
                print "Done"
            else:
                print "Bye!"

def main():
    pull_servers()

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function

