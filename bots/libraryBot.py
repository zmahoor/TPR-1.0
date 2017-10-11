from settings import *
import database
import re
import datetime


# !r !g !b
def validPrefix():
    global validColors
    return ["!"+color[0] for color in validColors] + ["!"+specialColor[0]]


# !rn 
def isRewardSignal(string):
    global validColors
    validRS = [p+"y" for p in validPrefix()]+[p+"n" for p in validPrefix()] +\
              [p+"l" for p in validPrefix()]+[p+"d" for p in validPrefix()]
    return string in validRS


def isCommand(data):
    global minCommandLength
    global maxCommandLength
    global validColors

    if "http" in data: return False
    if len(data) > maxCommandLength+1: return False
    if len(data) < minCommandLength+1: return False

    # if(data.startswith(tuple(validPrefix()))): return True
    if data[0] == "!": return True
    return False

# data = !rn  ==> color = data[1] and reward = data[2]
def parseReward(data):
    return data[1], data[2]


# data = !go ==> command = data[1:]
def parseCommand(data):
    return data[1:]


def getParentInfo(data):
    return data[1:]


db = database.DATABASE()
db.Flush_Old_Unprocessed_Chats()

while True:

    newRow = db.Fetch_An_Unprocessed_Chat()

    # print("newRow: ", newRow)

    if newRow is None: continue
   
    timeArrival, user, message = newRow['timeArrival'], newRow['username'], newRow['txt']

    # print newRow
    # check the user table and if the user is new then insert it
    db.Add_To_User_Table(user, timeArrival)
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), newRow

    # if this message is the user's first contribution--reward or command--, 
    # mark that in the help table. helpBot will later send a message to this user.
    if isRewardSignal(message) or isCommand(message):
        if db.First_Time_Contributer(user):
            print(message, 'first time contribution')
            db.Add_To_Help_Table(user, "first_time_contribution", timeArrival)

    if message[0] == '?':
        db.Add_To_Help_Table(user, message, timeArrival)
        print(message, " help requested.")

    # Or reinforcement then move to reinforcements table
    elif isRewardSignal(message):
        print(message, " reward entered.")
        color, reward = parseReward(message)
        db.Add_To_RewardLog_Table(user, color, reward, timeArrival)
        db.Add_Reward_To_Display_Table(color, reward, timeArrival)
        db.Update_Robot_Feedback(color, reward, timeArrival)

    # Either command then move to commands table
    elif isCommand(message):
        print(message, " command entered.")
        command = parseCommand(message)
        db.Add_To_CommandLog_Table(user, command, timeArrival)
        randIndex = db.Get_New_Word_Vector()
        # print command, timeArrival, randIndex
        db.Add_To_Unique_Commands_Table(command, timeArrival, randIndex)

    else:
        print(message, " discarded.")



