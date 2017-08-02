#!/usr/bin/python
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import os
import sys
import requests
import sqlite3
import time
from lxml import html







def gensched(gconnumeric):

    eventurl = 'https://www.gencon.com/events/'+ gconnumeric
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    print(eventurl)
    eventhead = requests.head(eventurl,headers=headers)
    print(eventhead.status_code)
    if eventhead.status_code == 200:

        eventdata = requests.get(eventurl,headers=headers)
        eventtree = html.fromstring(eventdata.content)
        eventelements = eventtree.xpath('//div[@class="value-full"]/text()')
        eventtitles = eventtree.xpath('//div[@class="name"]/text()')

        eventtimes = eventtree.xpath('//a[@title="Find other events on this day"]/text()')
        #div class='page-title'
        eventpage = eventtree.xpath('//div[@class="page-title"]/text()')
        eventtype = eventtree.xpath('//a[@title="Find other events of this type"]/text()')
        eventrules = eventtree.xpath('//a[@title="Find other events using this game system"]/text()')


       # (15, '$0.00')
       # (14, '\nNo, this is not a tournament.\n')
       # (13, 'Billie Jean Barry')
       # (12, '\nLucas Oil\n: Mtg Rm 1\n\n')
       # (11, '\n2\nhours\n')
       # (10, '\nYes, materials are provided for this game. You do not need to bring your own.\n')
       # (9, "None (You've never played before - rules will be taught)")
       # (8, 'Teen (13+)')
       # (7, '60')
       # (6, '1')
       # (5,
       #  'Dubbed-Vash the Stampede is an expert marksman who tries to promote "love and peace" but his reputation according to the public is questionable')
       # (4, '\n')
       # (3, '\n')
       # (2, '\n')
       # (1, '\n')
       # (0, 'ANI17123235')
        if len(eventelements) > 0:
            gameid = eventelements[0]
            gamecost = eventelements[-2]
            gamegm = eventelements[-4]
	    if ':' in eventelements[-5]:
                gamelocation = eventelements[-5].replace('\n', '')
	    if ':' in eventelements[-4]:
                gamelocation = eventelements[-4].replace('\n', '')
	    if ':' in eventelements[-3]:
                gamelocation = eventelements[-3].replace('\n', '')
            gameduration = eventelements[-6]
            gamemaxp = eventelements[-10]
            gameminp = eventelements[-11]
            gamedescription = eventelements[5]
        else:
            gameid, gamecost, gamegm, gamelocation, gameduration, gamemaxp, gameinp, gamedescription = "","","","","","","",""
        if len(eventtimes) > 0:
            gamestart = eventtimes[0]
            gameend = eventtimes[1]
        else:
            gamestart = 0
            gameend = 0

        if len(eventtitles) > 0:
            gamename = eventtitles[0]
        else:
            gamename = "No Title"

        if len(eventtype) > 0:
            gametype = eventtype[0]
        else:
            gametype = "No Type"

        if len(eventpage) > 0:
            gametitle = eventpage[0]
        else:
            gametitle = "No Title"

        if len(eventrules) > 0:
            gamerules = eventrules[0]
        else:
            gamerules=" "
	updatenow = int(time.time())
        #updatenow = (time.strftime("%Y/%m/%d %I:%M:%S"))
        conn = sqlite3.connect('/conbot/CONbot/gendb')
	eventlen = len(eventelements)
        blobby = str()
        #print blob
        print(gameid, gametitle, gamedescription, gamelocation, gametype, gamegm, gamestart, gameend, gamerules,eventurl,updatenow, eventlen)
       	#print(eventelements[-1],eventelements[-2],eventelements[-3],eventelements[-4],eventelements[-5],eventelements[-6],eventelements[-7],eventlen) 
	conn.execute("REPLACE INTO EVENTS (GAMEID, GAMETITLE, GAMEDESCRIPTION, GAMELOCATION, GAMETYPE, GAMEGM, GAMESTART, GAMEEND, GAMERULES, GCONWEB, UPDATED, BLOB) \
             VALUES (?,?,?,?,?,?,?,?,?,?,?,0)",(gameid, gametitle, gamedescription, gamelocation, gametype, gamegm, gamestart, gameend, gamerules,eventurl,updatenow));
        #cur.execute("insert into contacts (name, phone, email) values (?, ?, ?)",
            #(name, phone, email))
        conn.commit()
        conn.close()

gensched(sys.argv[1])
