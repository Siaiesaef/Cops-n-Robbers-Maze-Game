from sqlite3 import *
from passwordFunctions import *
 
def addPlayer(Username,Password):
    #hash the password using a custom hash function 
    hashed=customHash(Password)
    mydb=connect("Game.db")
    c=mydb.cursor()
    #stores the username and password in the database
    #uses parameters as every one entered will differ
    c.execute('''
INSERT INTO tblPlayerInf
VALUES(?,?)''',(Username,hashed))
    mydb.commit()
    mydb.close()

def usernameExists(Username):
    mydb=connect("Game.db")
    c=mydb.cursor()
    #check if the username already exists in the database
    #if not, return false
    #if it does, return true
    #uses parameters as every one entered will differ
    c.execute('''
SELECT *
FROM tblPlayerInf
WHERE Username=?''',(Username,))
    result=c.fetchone()
    mydb.close()
    return result is not None 

def deletePlayer(Username,Password):
    #hash the password using a custom hash function 
    hashed=customHash(Password)
    mydb=connect("Game.db")
    c=mydb.cursor()
    #delete the user from the database
    #uses parameters as every one entered will differ
    c.execute('''
DELETE FROM tblPlayerInf 
WHERE Username=? AND Password=?
    ''',(Username,hashed))
    mydb.commit()
    mydb.close()

def UpdateUsernameEasyLB(Username):
    mydb=connect("Game.db")
    c=mydb.cursor()
    #update the username in the leaderboard to "deleted user"
    #this is done to keep the leaderboard intact and not delete the scores
    #uses parameters as every one entered will differ
    c.execute('''
UPDATE tblEasyLB
SET Username="deleted user"
WHERE Username=?
    ''',(Username,))
    mydb.commit()
    mydb.close() 

def UpdateUsernameHardLB(Username):
    mydb=connect("Game.db")
    c=mydb.cursor()
    #update the username in the leaderboard to "deleted user"
    #this is done to keep the leaderboard intact and not delete the scores
    #uses parameters as every one entered will differ
    c.execute('''
UPDATE tblHardLB
SET Username="deleted user"
WHERE Username=?
    ''',(Username,))
    mydb.commit()
    mydb.close() 

def authenticateUser(Username,Password):
    #hash the password using a custom hash function 
    hashed=customHash(Password)
    mydb=connect("Game.db")
    c=mydb.cursor()
    #checks if the username and password match in the database
    #if they do, return true
    #uses parameters as every one entered will differ 
    c.execute('''
SELECT *
FROM tblPlayerInf
WHERE username=? AND password=?
    ''',(Username,hashed))
    results=c.fetchall()
    mydb.close()
    if len(results)==1:
        return True
    else:
        return False

def SeeEasyLeaderBoard():
    mydb=connect("Game.db")
    c=mydb.cursor()
    #fetches the top 10 players from the leaderboard
    #orders them by time in ascending order
    #displays the username, playertime and score
    c.execute('''
SELECT Username,PlayerTime,Score
FROM tblEasyLB
ORDER BY PlayerTime ASC
LIMIT 10
        ''')
    results=c.fetchall()
    mydb.commit()
    mydb.close() 
    #formats the results into a string to be displayed in the leaderboard
    #each result is formatted as "1.Username | PlayerTime | Score"
    formatted = "\n".join([f"{i+1}.{r[0]} | {r[1]} | {r[2]}" for i,r in enumerate(results)])
    return formatted

def SeeHardLeaderBoard():
    mydb=connect("Game.db")
    c=mydb.cursor()
    #fetches the top 10 players from the leaderboard
    #orders them by time in ascending order
    #displays the username, playertime and score
    c.execute('''
SELECT Username,PlayerTime,Score 
FROM tblHardLB
ORDER BY PlayerTime ASC
LIMIT 10
        ''')
    results=c.fetchall()
    mydb.commit()
    mydb.close()  
    #formats the results into a string to be displayed in the leaderboard
    #each result is formatted as "1.Username | PlayerTime | Score"   
    formatted = "\n".join([f"{i+1}.{r[0]} | {r[1]} | {r[2]}" for i,r in enumerate(results)])
    return formatted

def addEasyLB(Username,PlayerTime,Score):
    mydb=connect("Game.db")
    c=mydb.cursor()
    #adds the player to the leaderboard
    #the player is added to the leaderboard with their username, time and score
    #uses parameters as every one entered will differ 
    c.execute('''
INSERT INTO tblEasyLB(Username,PlayerTime,Score)
VALUES(?,?,?)''',(Username,PlayerTime,Score))
    mydb.commit()
    mydb.close()     

def addHardLB(Username,PlayerTime,Score):
    mydb=connect("Game.db")
    c=mydb.cursor()
    #adds the player to the leaderboard
    #the player is added to the leaderboard with their username, time and score
    #uses parameters as every one entered will differ 
    c.execute('''
INSERT INTO tblHardLB(Username,PlayerTime,Score)
VALUES(?,?,?)''',(Username,PlayerTime,Score))
    mydb.commit()
    mydb.close() 

