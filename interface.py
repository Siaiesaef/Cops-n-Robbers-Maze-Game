from appJar import gui
from sqlite3 import *
from SQL import * 
from appjarGui import * # import the appjarGui module to use the gui functions
#in a separate file to avoid circular imports 


##############################
########  INTERFACE  #########
##############################

#username= user
#password= Siaxmba24.

#decides what each button does for Main Screen
def press(btn):
    if btn=="Login":
        app.showSubWindow("Login")
        app.hide()
        return
    
    elif btn=="Create User":
        app.showSubWindow("Create User")
        app.hide()
        return
    
    elif btn=="Delete Account":
        app.showSubWindow("Delete Account")
        app.hide()
        return
    
    elif btn=="Quit":
        app.stop()
        return


#decides what each button does for Login Screen 
def LoginBtns(btn):
    if btn=="Go Back":
        app.show()
        app.hideSubWindow("Login")
        return
    
    elif btn=="Continue":
        Username=app.getEntry("Username: ")
        Password=app.getEntry("Password: ")
        #if the username and password are in the system, show game screen
        #and hide the login screen
        if authenticateUser(Username,Password)==True:
            app.hideSubWindow("Login")
            #hides login screen and starts game screen
            app.showSubWindow("Game")
            app.hide()
            return
        
        #if the username and password are not in the system, show error message
        #and return to login screen 
        elif authenticateUser(Username,Password)==False:
            app.errorBox("Error!","User is not in the system or password is invalid!")
            return


#descides what each button does for create user screen
def user(btn):
    if btn=="Return":
        app.show()
        app.hideSubWindow("Create User")

    elif btn=="Create":
        Username=app.getEntry("New Username: ").lower() 
        pass1=app.getEntry("New Password: ") 
        pass2=app.getEntry("Confirm Password: ")

        #check is the user already exists in the system
        #if the username is already taken, show error message and return to create user screen
        if usernameExists(Username):
            app.errorBox("Error!","That username has already been taken!")
            return

        #if the username is not taken, check if the password meets the criteria
        #if the password is weak, show error message and return to create user screen 
        if not strongPassword(pass1):
            app.errorBox(
                "Weak password!",
                "Password must contain at least 8 characters,\n"
                "including 1 uppercase character, 1 number and 1 special character."
            )
            return

        #checks if the password meets the criteria 
        elif strongPassword(pass1):
            #if it does then checks if they're the same
            #if the passwords are not the same, show error message and return to create user screen
            if pass1!=pass2:
                app.errorBox("Error!","Passwords don't match!")
                return
            
            #if the passwords are the same, add the user to the system 
            elif pass1==pass2:
                Password=pass1
                addPlayer(Username,Password)
                app.hideSubWindow("Create User")
                app.show()
                return


#decides what each button does for login screen 
def delete(btn):
    if btn=="Back":
        app.show()
        app.hideSubWindow("Delete Account")

    elif btn=="Delete":
        #get the username and password from the user
        Username=app.getEntry("Username to delete: ")
        Password=app.getEntry("Password to delete: ")

        #check if the username and password are in the system
        #if the username and password are in the system, delete the user from the system
        if authenticateUser(Username,Password)==True:
            deletePlayer(Username,Password)
            UpdateUsernameEasyLB(Username)
            UpdateUsernameHardLB(Username)
            app.infoBox("Success!","Account successfully deleted.")
            app.hideSubWindow("Delete Account")
            app.show()

        #if the username and password are not in the system, show error message
        #and return to delete account screen 
        elif authenticateUser(Username,Password)==False:
            app.errorBox("Error!","Details do not match!")


#decides what each button does for the you lose game over screen 
def gameOverL(btn):
    if btn=="Quit Game":
        app.stop()

    #if the player clicks play again, hide the game over screen and show the game screen 
    elif btn=="Play again":
        app.hideSubWindow("Game Over")
        app.showSubWindow("Game")


#decides what each button does for the you win game over screen 
def gameOverW(btn):
    if btn=="Quit Game ":
        app.stop()

    #if the player clicks play again, hide the game over screen and show the game screen
    elif btn=="Play again ":
        app.hideSubWindow("Game Over ")
        app.showSubWindow("Game")


#decides what each button does for the leaderboard screen
def leaderboard(btn):
    #if the player clicks easy, show the easy leaderboard
    if btn=="Easy":
        app.hideSubWindow("Leaderboard")
        app.showSubWindow("Easy leaderboard") 
        EasyLD_data=SeeEasyLeaderBoard()
        app.setLabel("EasyLeaderboard",EasyLD_data)

    #if the player clicks hard, show the hard leaderboard
    elif btn=="Hard":
        app.hideSubWindow("Leaderboard")
        app.showSubWindow("Hard leaderboard")
        HardLB_data=SeeHardLeaderBoard()
        app.setLabel("HardLeaderboard",HardLB_data)

    #if the player clicks return back, hide the leaderboard screen and show the game screen  
    elif btn=="Return Back":
        app.hideSubWindow("Leaderboard")
        app.showSubWindow("Game")


#decides what each button does for the game screen
def play(btn):
    #if the player clicks start game, hide the game screen and show the difficulty screen
    if btn=="Start Game":
        app.hideSubWindow("Game")
        app.showSubWindow("Difficulty")

    #if the player clicks view leaderboards, hide the game screen and show the leaderboard screen
    elif btn=="View Leaderboards":
        app.hideSubWindow("Game")
        app.showSubWindow("Leaderboard")

    #if the player clicks back, hide the game screen and show the login screen 
    elif btn=="back":
        app.hideSubWindow("Game")
        app.showSubWindow("Login")


#decides what each button does for the difficulty screen for the level of the game 
def choice(btn):
    from game import startGame # import the startGame function from game.py so that theres no circular import

    #if the player clicks easy, hide the difficulty screen and start the game with easy difficulty
    if btn=="Easy ":
        app.hideSubWindow("Difficulty")
        # username=
        startGame(rows=10,cols=10,difficulty="Easy")

    #if the player clicks hard, hide the difficulty screen and start the game with hard difficulty
    elif btn=="Hard ":
        app.hideSubWindow("Difficulty")
        startGame(rows=13,cols=13,difficulty="Hard")
        
    #if the player clicks return back, hide the difficulty screen and show the game screen
    elif btn==" Return Back":
        app.hideSubWindow("Difficulty")
        app.showSubWindow("Game")


#decides what the back button does for the easy leaderboard screen 
def easy(btn):
    if btn=="Back.":
        app.hideSubWindow("Easy leaderboard")
        app.showSubWindow("Leaderboard")


#decides what the back button does for the hard leaderboard screen
def hard(btn):
    if btn=="Back ":
        app.hideSubWindow("Hard leaderboard")
        app.showSubWindow("Leaderboard")


def startPage():
    #login page details
    app.setTitle("Main Screen")
    #makes size of the window same as size of background picture
    app.setSize(1200,600)
    #sets the background image for the main screen
    app.setBgImage("sc_bg.gif")
    #centers the window on the screen 
    app.setLocation(200,100)
    app.setSticky("s")
    app.addButton("Login", press,row=40,column=0)
    app.addButton("Create User", press,row=40,column=1)
    app.addButton("Delete Account", press,row=41,column=1)
    app.addButton("Quit",press,row=41,column=0)

    #calls all the subwindows 
    #subwindows are hidden by default 
    GameOverLSubwindow()
    GameOverWSubwindow()
    deleteAccountSubwindow()
    createUserSubwindow()
    loginSubwindow()
    leaderboardSubwindow()
    HardLeaderboard()
    EasyLeaderboard()  
    gamePage() 
    chooseDifficulty()

#subwindow for choosing difficulty for viewing the coressponding leaderboard
def chooseDifficulty():
    app.startSubWindow("Difficulty")
    app.setFont(size=20)
    app.addLabel("Choose Difficulty: ")
    app.addButtons(["Easy ","Hard "],choice)
    app.addButton(" Return Back",choice)
    app.stopSubWindow()

#subwindow for game screen
def gamePage():
    app.startSubWindow("Game")
    app.setFont(size=20)
    app.setTitle("Game")
    app.addButton("Start Game", play)
    app.addButton("View Leaderboards", play)
    app.addButton("back",play)
    app.stopSubWindow()

#subwindow for hard leaderboard screen
def HardLeaderboard():
    app.startSubWindow("Hard leaderboard")
    app.setFont(size=20)
    app.addLabel("HardLeaderboard","Top 10 Players") 
    app.addButton("Back ",hard)
    app.stopSubWindow()

#subwindow for easy leaderboard screen
def EasyLeaderboard():
    app.startSubWindow("Easy leaderboard")
    app.setFont(size=20)
    app.addLabel("EasyLeaderboard","Top 10 Players")
    app.addButton("Back.",easy)
    app.stopSubWindow()

#subwindow for leaderboard screen 
def leaderboardSubwindow():
    #subwindow for leaderboard screen
    app.startSubWindow("Leaderboard")
    app.setFont(size=20)
    app.setFont(40)
    app.addLabel("Leaderboard","Top 10 Players")
    app.setFont(10) 
    app.addLabel("Select Difficulty: ")
    app.addButtons(["Easy","Hard"],leaderboard)
    app.addButton("Return Back",leaderboard)
    app.stopSubWindow()

#subwindow for login screen
def loginSubwindow():
    #subwindow for login screen
    app.startSubWindow("Login",modal=True)
    app.setFont(size=20)
    app.addLabelEntry("Username: ")
    app.addLabelSecretEntry("Password: ")
    app.addButtons(["Go Back","Continue"],LoginBtns)
    app.stopSubWindow()

#subwindow for create user screen
def createUserSubwindow():
    #subwindow for create user screen
    app.startSubWindow("Create User")
    app.setFont(size=20)
    app.addLabelEntry("New Username: ")
    app.addLabelEntry("New Password: ")
    app.addLabelEntry("Confirm Password: ")
    app.addButtons(["Return","Create"],user)
    app.stopSubWindow()

#subwindow for delete account screen
def deleteAccountSubwindow():
    #subwindow for delete account screen
    app.startSubWindow("Delete Account")
    app.setFont(size=20)
    app.addLabelEntry("Username to delete: ")
    app.addSecretLabelEntry("Password to delete: ")
    app.addButtons(["Back","Delete"],delete)
    app.stopSubWindow()

#subwindow for game over screen when the player loses
def GameOverLSubwindow():
    app.startSubWindow("Game Over")
    app.setFont(size=20)
    app.addFlashLabel("You Lose, Game Over!!")
    app.addButtons(["Play again","Quit Game"],gameOverL)
    app.stopSubWindow()

#subwindow for game over screen when the player wins
def GameOverWSubwindow():
    app.startSubWindow("Game Over ")
    app.setFont(size=20)
    app.addFlashLabel("You Win, Game Over!!")
    app.addButtons(["Play again ","Quit Game "],gameOverW)
    app.stopSubWindow()

#runs the app and starts the main screen 
#as the other subwindows are hidden by default
startPage()  
app.go()