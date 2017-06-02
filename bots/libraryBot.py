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

    validRS = [p+"y" for p in validPrefix()]+[p+"n" for p in validPrefix()]+\
    [p+"l" for p in validPrefix()]+[p+"d" for p in validPrefix()]

    return string in validRS

def isCommand(data):
    global minCommandLength
    global maxCommandLength
    global validColors

    if "http" in data: return False
 
    if (len(data) > maxCommandLength+1 ): return False
    if (len(data) < minCommandLength+1): return False

    # if(data.startswith(tuple(validPrefix()))): return True
    if(data[0] == "!"): return True

    return False

#data = !rn  ==> color = data[1] and reward = data[2]
def parseReward(data):
    return data[1], data[2]

#data = !go ==> command = data[1:]
def parseCommand(data):
    return data[1:]

def getParentInfo(data):
    return data[1:]

mydatabase = database.DATABASE();

while(True):

    newRow = mydatabase.Fetch_An_Unprocessed_Chat()

    # print("newRow: ", newRow)

    if newRow == None: continue
   
    timeArrival = newRow['timeArrival']
    user = newRow['username']
    message = newRow['txt']

    # check the user table and if the user is new then insert it
    mydatabase.Add_To_User_Table(user, timeArrival)

    #message begins with '?' send message to helpbot to chat to user
    if (message[0] == '?'):

        mydatabase.Add_To_Help_Table(user, message, timeArrival)

        print(message, " help requested.")
    
    #set the username after @ as the parent of this user
    elif (message[0] == '#'):

        print(message, " set parent.")

        parent = getParentInfo(message)

        mydatabase.Update_User_Parent(user, parent)

    #Or reinforcement then move to reinforcements table
    elif isRewardSignal(message):

        print(message, " reward entered.")

        color, reward = parseReward(message)

        mydatabase.Add_To_RewardLog_Table(user, color, reward, timeArrival)

        mydatabase.Add_Reward_To_Display_Table(color, reward, timeArrival)

        mydatabase.Update_Total_Fitness(color, reward, timeArrival)

        mydatabase.Update_Total_Likeability(color, reward, timeArrival)

    #Either command then move to commands table
    elif isCommand(message):

        print(message, " command entered")

        command = parseCommand(message)

        mydatabase.Add_To_CommandLog_Table(user, command, timeArrival)

        randIndex = mydatabase.Get_New_WordIndex()

        # print command, timeArrival, randIndex

        mydatabase.Add_To_Unique_Commands_Table(command, timeArrival, randIndex)

    else:
        #if does not start with ? or !, it is raw chat
        message_type = 0
        #keep in chats table???


