#!/usr/bin/python
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import json
import os
import sys
import requests
import sqlite3
import re
import subprocess 
@respond_to('help', re.IGNORECASE)
def hi(message):
    message.reply('Try (regex) at (day) (hour), or events (regex for event type) (day) (regex-one word only cuz lazy) ')
    # react with thumb up emoji
    message.react('+1')

@respond_to('(.*) on (.*) (.*)', re.IGNORECASE)
def health(message, regexstuff, regextwo, regexthree="regextwo"):
    # Message is sent on the channel
    message.send('Looking...')
    conn = sqlite3.connect('/conbot/CONbot/gendb')

    cursor=conn.cursor()

    eventid="%" + regexstuff + "%"
    eventday="%" + regextwo + "%"
    eventtime="%" + regexthree + "%"
    cursor.execute('SELECT GAMEID, GAMETITLE, GAMEDESCRIPTION, GAMELOCATION, GAMESTART, GCONWEB, UPDATED FROM EVENTS where (GAMEDESCRIPTION LIKE "{event}" OR GAMERULES LIKE "{event}" OR GAMETITLE LIKE "{event}" OR GAMELOCATION LIKE "{event}") AND GAMESTART LIKE "{eventday}" AND GAMESTART LIKE "{eventtime}"'.format(event=eventid,eventday=eventday,eventtime=eventtime))
    all_rows = cursor.fetchall()
    unshown=0
    addtitle = ['']
    linecount=0
    for row in all_rows:
        linecount=linecount + 1
        if linecount > 5:
           unshown = unshown + 1
           if title not in addtitle:
                addtitle.append(title)
        else:
            id, title, description, location, start, gconweb, updated = row
            attachments = [
            {
            "fallback": "Event Description",
            "color": "#36a64f",
            "pretext": "CONbot",
            "author_name": id,
            "author_link": gconweb,
            "title": title,
            "title_link": gconweb,
            "text": description,
            "fields": [
                {
                    "title":  location,
                    "value": start,
                    "short": "false"
                }
            ],
            "footer": "CONbot",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": updated
            }
            ]



            message.send_webapi('', json.dumps(attachments))
           # message.reply("ID:" + id + " TITLE:" + title + " LOCATION:" + location + " START:" + start + "\nDESCRIPTION:" + description +"\n" + gconweb)
    conn.close()
    message.reply("Total of " + str(unshown) + " additional matching events found.")
    titelen=len(addtitle)
    #message.reply(addtitle[0:titelen])




@respond_to('events (.*) (.*) (.*)', re.IGNORECASE)
def health(message, regexstuff, regextwo, regexthree="Null"):
    # Message is sent on the channel
    message.send('Looking...')
    conn = sqlite3.connect('/conbot/CONbot/gendb')

    cursor=conn.cursor()

    eventid="%" + regexthree + "%"
    eventtype="%" + regexstuff + "%"
    eventday="%" + regextwo + "%"
    cursor.execute('SELECT GAMEID, GAMETITLE, GAMEDESCRIPTION, GAMELOCATION, GAMESTART, GCONWEB, UPDATED FROM EVENTS where (GAMEDESCRIPTION LIKE "{event}" OR GAMERULES LIKE "{event}" OR GAMETITLE LIKE "{event}" OR GAMELOCATION LIKE "{event}") AND GAMETYPE LIKE "{eventtype}" AND GAMESTART LIKE "{eventday}"'.format(event=eventid,eventtype=eventtype,eventday=eventday))
    all_rows = cursor.fetchall()
    unshown=0
    addtitle = ['']
    linecount=0
    for row in all_rows:
        linecount=linecount + 1
        if linecount > 5:
           unshown = unshown + 1
           if title not in addtitle:
                addtitle.append(title)
        else:
            id, title, description, location, start, gconweb, updated = row
            attachments = [
            {
            "fallback": "Event Description",
            "color": "#36a64f",
            "pretext": "CONbot",
            "author_name": id,
            "author_link": gconweb,
            "title": title,
            "title_link": gconweb,
            "text": description,
            "fields": [
                {
                    "title":  location,
                    "value": start,
                    "short": "false"
                }
            ],
            "footer": "CONbot",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": updated 
            }
            ]



            message.send_webapi('', json.dumps(attachments))
           # message.reply("ID:" + id + " TITLE:" + title + " LOCATION:" + location + " START:" + start + "\nDESCRIPTION:" + description +"\n" + gconweb)
    conn.close()
    message.reply("Total of " + str(unshown) + " additional matching events found.")
    titelen=len(addtitle)
    #message.reply(addtitle[0:titelen])
def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
