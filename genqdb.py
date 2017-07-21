#!/usr/bin/python
import sys
import sqlite3

conn = sqlite3.connect('./gendb')
print "Opened database successfully";

#conn.execute('''CREATE TABLE EVENTS 
#         (ID     TEXT  PRIMARY KEY   NOT NULL,
#	 WEBEVENT 	TEXT ,
#         TITLE           TEXT    ,
#         HOURS           TEXT     ,
#         DESCRIPTION        CHAR(255) ,
#         LOCATION           CHAR(100) ,
#	 TYPE		 TEXT	,
#	 START		CHAR(50),
#	 END		CHAR(50),
#	 SYSTEM		CHAR(50),
#	 TICKETS	TEXT	);''')
#         (GAMEID     TEXT  PRIMARY KEY   NOT NULL,
#	 GAMETITLE 	BLOB,
#         GAMEDESCRIPTION           BLOB    ,
#         GAMELOCATION           BLOB     ,
#	 GAMETYPE	BLOB ,
#	 GAMEGM		BLOB ,
#	 GAMESTART	BLOB ,
#	 GAMEEND	BLOB ,
#	 GAMERULES	BLOB ,
#	 BLOB	BLOB	);''')
#print "Table created successfully";
cursor=conn.cursor()
eventid="%" + sys.argv[3] + "%"
eventtype="%" + sys.argv[1] + "%"
eventday="%" + sys.argv[2] + "%"
cursor.execute('SELECT GAMEID, GAMETITLE, GAMEDESCRIPTION, GAMELOCATION, GAMESTART, GCONWEB FROM EVENTS where (GAMEDESCRIPTION LIKE "{event}" OR GAMERULES LIKE "{event}" OR GAMETITLE LIKE "{event}" OR GAMELOCATION LIKE "{event}") AND GAMETYPE LIKE "{eventtype}" AND GAMESTART LIKE "{eventday}"'.format(event=eventid,eventtype=eventtype,eventday=eventday))
all_rows = cursor.fetchall()


for row in all_rows:
	id, title, description, location, start, gconweb = row
        print "ID:" + id + " TITLE:" + title + " LOCATION:" + location + " START:" + start + "\nDESCRIPTION:" + description +"\n" + gconweb
conn.close()
