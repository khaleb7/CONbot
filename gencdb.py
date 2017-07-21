#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('./gendb')
print "Opened database successfully";


conn.execute('''CREATE TABLE EVENTS 
         (GAMEID     TEXT  PRIMARY KEY   NOT NULL,
	 GAMETITLE 	BLOB,
         GAMEDESCRIPTION           BLOB    ,
         GAMELOCATION           BLOB     ,
	 GAMETYPE	BLOB ,
	 GAMEGM		BLOB ,
	 GAMESTART	BLOB ,
	 GAMEEND	BLOB ,
	 GAMERULES	BLOB ,
	 GCONWEB	BLOB ,
	 UPDATED	DATE ,
	 BLOB	BLOB	);''')
print "Table created successfully";

conn.close()

