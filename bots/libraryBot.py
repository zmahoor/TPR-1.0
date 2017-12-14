"""
this script reads all the rows from the chat table and places them into their right tables.
"""
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
    validRS = [p+"y" for p in validPrefix()]+[p+"n" for p in validPrefix()]+\
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
db.flush_old_unprocessed_chats()

while True:
    newRow = db.fetch_unprocessed_chat()
    # print("newRow: ", newRow)
    if newRow is None: continue
    timeArrival, user, message = newRow['timeArrival'], newRow['username'], newRow['txt']

    # print newRow
    # check the user table and if the user is new then insert it
    db.add_to_user_table(user, timeArrival)
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), newRow

    # if this message is the user's first contribution--reward or command--, 
    # mark that in the help table. helpBot will later send a message to this user.
    if isRewardSignal(message) or isCommand(message):
        if db.first_time_contributer(user):
            print(message, 'first time contribution')
            db.add_to_help_table(user, "first_time_contribution", timeArrival)

    if message[0] == '?':
        db.add_to_help_table(user, message, timeArrival)
        print(message, " help requested.")

    # Or reinforcement then move to reinforcements table
    elif isRewardSignal(message):
        print(message, " reward entered.")
        color, reward = parseReward(message)
        db.add_to_Reward_log_table(user, color, reward, timeArrival)
        db.add_reward_to_display_table(color, reward, timeArrival)
        db.update_robot_feedback(color, reward, timeArrival)

    # Either command then move to commands table
    elif isCommand(message):
        print(message, " command entered.")
        command = parseCommand(message)
        db.add_to_command_log_table(user, command, timeArrival)
        randIndex = db.get_new_word_vector()
        # print command, timeArrival, randIndex
        db.add_to_unique_commands_table(command, timeArrival, randIndex)

    else:
        print(message, " discarded.")



