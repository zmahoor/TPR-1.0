from settings import *
import database;
from time import *
import re

# !r !g !b
def validPrefix():
    global validColors
    return [ "!"+color[0] for color in validColors]

# !rn 
def isRewardSignal(string):
    global validColors

    validRS = [ p+"y" for p in validPrefix() ] +\
            [ p+"n" for p in validPrefix() ]

    return string in validRS

def isCommand(data):
    global minCommandLength
    global maxCommandLength
    global validColors

    if "http" in data: return False
 
    if (len(data) > maxCommandLength+2 ): return False
    if (len(data) < minCommandLength+2): return False

    if(data.startswith(tuple(validPrefix()))): return True

    return False

#data = !rn  ==> color = data[1] and reward = data[2]
def parseReward(data):
    return data[1], data[2]

#data = !rgo ==> color = data[1] and command = data[2:]
def parseCommand(data):
    return data[1], data[2:]

def getParentInfo(data):
    return data[1:]

mydatabase = database.DATABASE();

message_type = 0

validColors = ['red', 'green', 'blue']
maxCommandLength = 50
minCommandLength = 2

while(True):

    newRow = mydatabase.Fetch_New_Chat()

    if newRow == None: continue
   
    timeArrival = newRow[1]
    user = newRow[2]
    message = newRow[3]

    # check the user table and if the user is new then insert it
    mydatabase.Add_User(user, timeArrival)

    #message begins with '?' send message to helpbot to chat to user
    if (message[0] == '?'):
        print(message, " help requested")
    #show the score table
    elif(message[0] == '_'):
        print(message, " score table")
    
    #set the username after @ as the parent of this user
    elif(message[0] == '@'):
        print(message, " set parent")
        parent = getParentInfo(message)
        mydatabase.Add_User_Parent(user, parent)

    #Or reinforcement then move to reinforcements table
    elif isRewardSignal(message):
        print(message, "reward signal")
        color, reward = parseReward(message)
        mydatabase.Add_Reinforcement(color, reward)

    #Either command then move to commands table
    elif isCommand(message):
        print(message, "command")
        color, command = parseCommand(message)
        mydatabase.Add_Command(command, color, timeArrival)

    else:
        #if does not start with ? or !, it is raw chat
        message_type = 0
        #keep in chats table???


