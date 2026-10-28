from sqlite3 import *

# This file creates the database and tables for the game
mydb=connect("Game.db")
#allows foreign keys to be used in the database 
mydb.execute("PRAGMA foreign_keys = ON")
c=mydb.cursor()

#Player Information table
c.execute('''
CREATE TABLE tblPlayerInf(
Username VARCHAR(25) PRIMARY KEY NOT NULL,
Password VARCHAR(25),
FOREIGN KEY (Username) REFERENCES tblEasyLB(Username),
FOREIGN KEY (Username) REFERENCES tblHardLB(Username) 
)
''')

#Easy leaderboard table
c.execute('''
CREATE TABLE tblEasyLB(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Username VARCHAR(25),
PlayerTime TIME(6),
Score VARCHAR(2),
FOREIGN KEY (Username) REFERENCES tblPlayerInf(Username)
)
''')

#Hard leaderboard table
c.execute('''
CREATE TABLE tblHardLB(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Username VARCHAR(25),
PlayerTime TIME(6),
Score VARCHAR(2),
FOREIGN KEY (Username) REFERENCES tblPlayerInf(Username)
)
''')

mydb.commit()
mydb.close()
