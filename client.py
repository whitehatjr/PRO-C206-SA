#-------------Boilerplate Code Start-----
import socket
from tkinter import *
from  threading import Thread
import random
from PIL import ImageTk, Image

screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None
canvas2 = None

nameEntry = None
nameWindow = None
gameWindow = None

leftBoxes = []
rightBoxes = []
finishingBox = None

playerType = None
playerTurn = None
player1Name = 'joining'
player2Name = 'joining'
player1Label = None
player2Label = None

player1Score = 0
player2Score = 0
player2ScoreLabel = None
player2ScoreLabel = None

dice = None

rollButton = None
resetButton = None

winingMessage = None

winingFunctionCall = 0

#-------------Boilerplate Code End-----


# Boilerplate Code
def checkColorPosition(boxes, color):
    for box in boxes:
        boxColor = box.cget("bg")
        if(boxColor == color):
            return boxes.index(box)
    return False

# Teacher Activity
def movePlayer1(steps):
    global leftBoxes

    boxPosition = checkColorPosition(leftBoxes[1:],"red")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(steps == remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            global finishingBox

            finishingBox.configure(bg='red')

            global SERVER
            global playerName

            greetMessage = f'Red wins the game.'
            SERVER.send(greetMessage.encode())

        elif(steps < remainingSteps):
            for box in leftBoxes[1:]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            leftBoxes[nextStep].configure(bg='red')
        else:
            print("Move False")
    else:
        # first step
        leftBoxes[steps].configure(bg='red')


# Student Activity
def movePlayer2(steps):
    global rightBoxes

    # Moving to reverse order
    tempBoxes = rightBoxes[-2::-1]

    boxPosition = checkColorPosition(tempBoxes,"yellow")

    if(boxPosition):
        diceValue = steps
        coloredBoxIndex = boxPosition
        totalSteps = 10
        remainingSteps = totalSteps - coloredBoxIndex

        if(diceValue == remainingSteps):
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')

            global finishingBox

            finishingBox.configure(bg='yellow', fg="black")

            global SERVER
            global playerName

            greetMessage = f'Yellow wins the game.'
            SERVER.send(greetMessage.encode())

        elif(diceValue < remainingSteps):
            for box in rightBoxes[-2::-1]:
                box.configure(bg='white')

            nextStep = (coloredBoxIndex + 1 ) + diceValue
            rightBoxes[::-1][nextStep].configure(bg='yellow')
        else:
            print("Move False")
    else:
        # first step
        rightBoxes[len(rightBoxes) - (steps+1)].configure(bg='yellow')



def rollDice():
    global SERVER
    #create a number variable in which the list of all the ASCII characters of the string will be stored
    #Use backslash because unicode must have a backslash
    diceChoices=['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']

    #configure the label
    value = random.choice(diceChoices)

    global playerType
    global rollButton
    global playerTurn

    rollButton.destroy()
    playerTurn = False

    if(playerType == 'player1'):
        SERVER.send(f'{value}player2Turn'.encode())

    if(playerType == 'player2'):
        SERVER.send(f'{value}player1Turn'.encode())





def leftBoard():
    global gameWindow
    global leftBoxes
    global screen_height

    xPos = 30
    for box in range(0,11):
        if(box == 0):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="red")
            boxLabel.place(x=xPos, y=screen_height/2 - 88)
            leftBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2- 100)
            leftBoxes.append(boxLabel)
            xPos +=75


def rightBoard():
    global gameWindow
    global rightBoxes
    global screen_height

    xPos = 988
    for box in range(0,11):
        if(box == 10):
            boxLabel = Label(gameWindow, font=("Helvetica",30), width=2, height=1, relief='ridge', borderwidth=0, bg="yellow")
            boxLabel.place(x=xPos, y=screen_height/2-88)
            rightBoxes.append(boxLabel)
            xPos +=50
        else:
            boxLabel = Label(gameWindow, font=("Helvetica",55), width=2, height=1, relief='ridge', borderwidth=0, bg="white")
            boxLabel.place(x=xPos, y=screen_height/2 - 100)
            rightBoxes.append(boxLabel)
            xPos +=75


def finishingBox():
    global gameWindow
    global finishingBox
    global screen_width
    global screen_height

    finishingBox = Label(gameWindow, text="Home", font=("Chalkboard SE", 32), width=8, height=4, borderwidth=0, bg="green", fg="white")
    finishingBox.place(x=screen_width/2 - 68, y=screen_height/2 -160)



def gameWindow():
    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global dice
    global winingMessage
    global resetButton


    gameWindow = Tk()
    gameWindow.title("Ludo Ladder")
    gameWindow.attributes('-fullscreen',True)

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/2, screen_height/5, text = "Ludo Ladder", font=("Chalkboard SE",100), fill="white")

    # ------------ Boilerplate Code

    # Declaring Wining Message
    winingMessage = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 250, text = "", font=("Chalkboard SE",100), fill='#fff176')

    # Creating Reset Button
    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)

    # ------------ Boilerplate End


    leftBoard()
    rightBoard()
    finishingBox()

    global rollButton

    rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)

    global playerTurn
    global playerType
    global playerName
    # Additional Activity
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel



    if(playerType == 'player1' and playerTurn):
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
    else:
        rollButton.pack_forget()

    # Creating Dice with value 1
    dice = canvas2.create_text(screen_width/2 + 10, screen_height/2 + 100, text = "\u2680", font=("Chalkboard SE",250), fill="white")

    # Creating name board
    player1Label = canvas2.create_text(400,  screen_height/2 + 100, text = player1Name, font=("Chalkboard SE",80), fill='#fff176' )
    player2Label = canvas2.create_text(screen_width - 300, screen_height/2 + 100, text = player2Name, font=("Chalkboard SE",80), fill='#fff176' )

    # Creating Score Board
    player1ScoreLabel = canvas2.create_text(400,  screen_height/2 - 160, text = player1Score, font=("Chalkboard SE",80), fill='#fff176' )
    player2ScoreLabel = canvas2.create_text(screen_width - 300, screen_height/2 - 160, text = player2Score, font=("Chalkboard SE",80), fill='#fff176' )


    gameWindow.resizable(True, True)
    gameWindow.mainloop()



def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()



def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Ludo Ladder")
    nameWindow.attributes('-fullscreen',True)


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/2, screen_height/5, text = "Enter Name", font=("Chalkboard SE",100), fill="white")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 50), bd=5, bg='white')
    nameEntry.place(x = screen_width/2 - 220, y=screen_height/4 + 100)


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=15, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/2 - 130, y=screen_height/2 - 30)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()


#--------- Boilerplate Code Start---------------
def restGame():
    global SERVER
    SERVER.send("reset game".encode())


def handleWin(message):
    global playerType
    global rollButton
    global canvas2
    global winingMessage
    global screen_width
    global screen_height
    global resetButton

    #destroying button
    if('Red' in message):
        if(playerType == 'player2'):
            rollButton.destroy()

    if('Yellow' in message):
        if(playerType == 'player1'):
            rollButton.destroy()

    # Adding Wining Message
    message = message.split(".")[0] + "."
    canvas2.itemconfigure(winingMessage, text = message)

    #Placing Reset Button
    resetButton.place(x=screen_width / 2 - 80, y=screen_height - 220)

def updateScore(message):
    global canvas2
    global player1Score
    global player2Score
    global player1ScoreLabel
    global player2ScoreLabel


    if('Red' in message):
        player1Score +=1

    if('Yellow' in message):
        player2Score +=1

    canvas2.itemconfigure(player1ScoreLabel, text = player1Score)
    canvas2.itemconfigure(player2ScoreLabel, text = player2Score)



def handleResetGame():
    global canvas2
    global playerType
    global gameWindow
    global rollButton
    global dice
    global screen_width
    global screen_height
    global playerTurn
    global rightBoxes
    global leftBoxes
    global finishingBox
    global resetButton
    global winingMessage
    global winingFunctionCall

    canvas2.itemconfigure(dice, text='\u2680')

    # Handling Reset Game
    if(playerType == 'player1'):
        # Creating roll dice button
        rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
        rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)
        playerTurn = True

    if(playerType == 'player2'):
        playerTurn = False

    for rBox in rightBoxes[-2::-1]:
        rBox.configure(bg='white')

    for lBox  in leftBoxes[1:]:
        lBox.configure(bg='white')


    finishingBox.configure(bg='green')
    canvas2.itemconfigure(winingMessage, text="")
    resetButton.destroy()

    # Again Recreating Reset Button for next game
    resetButton =  Button(gameWindow,text="Reset Game", fg='black', font=("Chalkboard SE", 15), bg="grey",command=restGame, width=20, height=5)
    winingFunctionCall = 0
#----------------- Boilerplate Code End ---------------


def recivedMsg():
    global SERVER
    global playerType
    global playerTurn
    global rollButton
    global screen_width
    global screen_height
    global canvas2
    global dice
    global gameWindow
    global player1Name
    global player2Name
    global player1Label
    global player2Label
    global winingFunctionCall



    while True:
        message = SERVER.recv(2048).decode()

        if('player_type' in message):
            recvMsg = eval(message)
            playerType = recvMsg['player_type']
            playerTurn = recvMsg['turn']
        elif('player_names' in message):

            players = eval(message)
            players = players["player_names"]
            for p in players:
                if(p["type"] == 'player1'):
                    player1Name = p['name']
                if(p['type'] == 'player2'):
                    player2Name = p['name']

        elif('⚀' in message):
            # Dice with value 1
            canvas2.itemconfigure(dice, text='\u2680')
        elif('⚁' in message):
            # Dice with value 2
            canvas2.itemconfigure(dice, text='\u2681')
        elif('⚂' in message):
            # Dice with value 3
            canvas2.itemconfigure(dice, text='\u2682')
        elif('⚃' in message):
            # Dice with value 4
            canvas2.itemconfigure(dice, text='\u2683')
        elif('⚄' in message):
            # Dice with value 5
            canvas2.itemconfigure(dice, text='\u2684')
        elif('⚅' in message):
            # Dice with value 6
            canvas2.itemconfigure(dice, text='\u2685')
        #--------- Boilerplate Code Start--------
        elif('wins the game.' in message and winingFunctionCall == 0):
            winingFunctionCall +=1
            handleWin(message)
            # Addition Activity
            updateScore(message)
        elif(message == 'reset game'):
            handleResetGame()
        #--------- Boilerplate Code End--------


        #creating rollbutton
        if('player1Turn' in message and playerType == 'player1'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 250)

        elif('player2Turn' in message and playerType == 'player2'):
            playerTurn = True
            rollButton = Button(gameWindow,text="Roll Dice", fg='black', font=("Chalkboard SE", 15), bg="grey",command=rollDice, width=20, height=5)
            rollButton.place(x=screen_width / 2 - 80, y=screen_height/2  + 260)


        # Student Activity
        # Deciding player turn
        if('player1Turn' in message or 'player2Turn' in message):
            diceChoices=['⚀','⚁','⚂','⚃','⚄','⚅']
            diceValue = diceChoices.index(message[0]) + 1

            if('player2Turn' in message):
                movePlayer1(diceValue)


            if('player1Turn' in message):
                movePlayer2(diceValue)

        # Additional Activity
        # Creating Name Board
        if(player1Name != 'joining' and canvas2):
            canvas2.itemconfigure(player1Label, text=player1Name)

        if(player2Name != 'joining' and canvas2):
            canvas2.itemconfigure(player2Label, text=player2Name)





def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 8000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()




setup()
