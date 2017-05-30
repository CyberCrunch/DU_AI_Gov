# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 11:08:44 2017

@author: robin
source: http://alvinalexander.com/python/python-script-read-rss-feeds-database
"""

#!/usr/bin/python

import feedparser
import time
from subprocess import check_output
import sys
import re

def clearRSS():
    db = 'feeds.txt'
    f = open(db, 'w')
    f.write("")
    f.close
        

def getRSSupdates(feed_name, url):
    db = 'feeds.txt'
    limit = 12 * 3600 * 1000
    
    #
    # function to get the current time
    #
    current_time_millis = lambda: int(round(time.time() * 1000))
    current_timestamp = current_time_millis()
    
    def post_is_in_db(title):
        with open(db, 'r') as database:
            for line in database:
                if title in line:
                    return True
        return False
    
    # return true if the title is in the database with a timestamp > limit
    def post_is_in_db_with_old_timestamp(title):
        with open(db, 'r') as database:
            for line in database:
                if title in line:
                    ts_as_string = line.split('|', 1)[1]
                    return True
        return False
    
    #
    # get the feed data from the url
    #
    feed = feedparser.parse(url)
    
    #
    # figure out which posts to print
    #
    posts_to_print = []
    posts_to_print_value = []

    posts_to_skip = []
    
    for post in feed.entries:
        # if post is already in the database, skip it
        title = post.title
        value = post.summary

        if post_is_in_db_with_old_timestamp(title):
            posts_to_skip.append(title)
        else:
            posts_to_print.append(title)
            posts_to_print_value.append(value)
       
    #
    # add all the posts we're going to print to the database with the current timestamp
    # (but only if they're not already in there)
    # 
    with open(db,'a') as f:        
        for title in posts_to_print:
            if not post_is_in_db(title):
                f.write(title + "|" + str(current_timestamp) + "\n")
        
    #
    # output all of the new posts
    #
    returnStr = ""
    count = 1
    
    for num in range(0,len(posts_to_print)):
        returnStr += ("\n" + time.strftime("%a, %b %d %I:%M %p") + ': ' + feed_name+"\n")
        returnStr += ("Title: " + posts_to_print[num] + "\n")
        returnStr += (posts_to_print_value[num] + "\n") 
        count += 1
    cleanr = re.compile('<.*?>')
    returnStr = re.sub(cleanr, '', returnStr)
    cleanr = re.compile('&nbsp;')
    returnStr = re.sub(cleanr, '', returnStr)
    returnStr = ''.join(i for i in returnStr if ord(i)<128) #remove nonASCII
   
    if returnStr == "":
        returnStr = "no new feeds"
    return returnStr
        
    
if __name__ == "__main__": #testing feeds
    print(getRSSupdates('vulture gaming', 'http://www.vulturecorporation.com/forum/m/20530240/op/rss/forum_id/3849082'))
    clearRSS()
    print(getRSSupdates('dual universe announcements', 'https://board.dualthegame.com/index.php/rss/forums/1-du-forum-rss-feed/'))
