import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE
import numpy as np
from random import shuffle, choice
from copy import deepcopy

def find_repeats(mylist):

    count = 0
    for i in range(1, len(mylist)):
        if mylist[i] == mylist[i-1]: count += 1
    return count

def random_list(mylen):
    return ['y' if np.random.uniform(0,1)> 0.5 else 'n' for i in range(mylen)]

db = DATABASE()

# sql="""SELECT displayID, count(*) as count FROM TwitchPlays.reward_log where 
# reward='y' or reward='n' group by displayID having count=2 and displayID is not NULL;"""
# records = db.Execute_Select_Sql_Command(sql, ' ')

# total         = 0
# disagreements = 0
# total_array   = []
# double_vote   = 0
# disagreements_with_yourself = 0

# for record in records:

#     displayID = record['displayID']
#     sql="""SELECT userName,reward FROM TwitchPlays.reward_log where 
#     (reward='y' or reward='n') and displayID=%d;"""%(displayID)

#     feedback  = db.Execute_Select_Sql_Command(sql, ' ')

#     if feedback[0]['userName'] == feedback[1]['userName']: 
#         double_vote += 1

#         if feedback[0]['reward'] != feedback[1]['reward']: 
#             disagreements_with_yourself += 1

#     if feedback[0]['userName'] != feedback[1]['userName']:
#         total += 1
#         total_array.append([int(feedback[0]['reward']=='y'), int(feedback[1]['reward']=='y')])

#         if feedback[0]['reward'] != feedback[1]['reward']: 
#             disagreements += 1

# print len(records), double_vote, disagreements_with_yourself, total, disagreements, float(disagreements)/total

# print np.array(total_array)
################################################################################

# sql="""SELECT displayID, count(*) as count FROM TwitchPlays.reward_log where 
# reward='y' or reward='n' group by displayID having count>=2 and displayID is not NULL;"""
# records = db.Execute_Select_Sql_Command(sql, ' ')

# total         = 0
# disagreements = 0
# reward_array  = []
# true_agreement_count = 0

# for record in records:

#     displayID = record['displayID']
#     sql="""SELECT userName,reward, timeArrival FROM TwitchPlays.reward_log where 
#     (reward='y' or reward='n') and displayID=%d order by timeArrival ASC;"""%(displayID)

#     feedback  = db.Execute_Select_Sql_Command(sql, ' ')

#     # print feedback

#     userNames = set([ f['userName'] for f in feedback ])
#     rewards   = [ f['reward'] for f in feedback ]
#     reward_array.append( rewards )

#     if len(userNames) < len(feedback): continue
#     true_agreement_count += find_repeats(rewards)
#     # print rewards, true_agreement_count

# # print reward_array
# random_agreement_count = []

# for i in range(0, 1000):

#     count = 0
#     for rewards in reward_array:
#         # shuffle(rewards)   
#         rewards = ['y' if np.random.uniform(0,1)> 0.5 else 'n' for i in range(len(rewards))]   
#         count  += find_repeats(rewards)

#     random_agreement_count.append(count)

# print "random count: ", np.percentile(random_agreement_count, 99), "true count: ", true_agreement_count

################################################################################

def count_disagreements( feedback ):

    # print feedback
    count = 0
    for key in feedback:
        if len(set(feedback[key]))>1:
            count += 1
    return count

def shuffle_feedback( feedback ):

    if len(feedback) == 1: return feedback
    # print "before shuffle: ", feedback

    rand_keys = np.random.choice(feedback.keys(), 2, replace=False)
    key1, key2 = rand_keys

    index1 = np.random.randint(0, len(feedback[key1]))
    index2 = np.random.randint(0, len(feedback[key2]))

    feedback[key1][index1], feedback[key2][index2] = feedback[key2][index2], feedback[key1][index1]
    # print "after shuffle: ", feedback

    return feedback

data = {}

sql="""SELECT robotID, cmdTxt from display where (numYes+numYes)>=2 group by robotID, cmdTxt;"""
records = db.execute_select_sql_command(sql, 'Failed fetch...')

for record in records:

    robotID = record['robotID']
    cmdTxt  = record['cmdTxt']

    # print record

    sql = """SELECT r.displayID, r.reward, d.robotID, d.cmdTxt, r.userName FROM 
    TwitchPlays.reward_log as r join TwitchPlays.display as d on d.displayID=r.displayID where 
    robotID=%d and cmdTxt='%s' and (r.reward='y' or r.reward='n');"""%(robotID, cmdTxt)

    evaluations = db.execute_select_sql_command(sql, 'Failed fetch...')

    if len(evaluations) < 2: continue
    # print evaluations
    # print

    robot_command_dict = {}

    for evals in evaluations:

        username  = evals['userName']
        reward    = evals['reward']
        displayID = evals['displayID']

        if displayID in robot_command_dict:
            robot_command_dict[displayID].append((username,reward))
        else:  robot_command_dict[displayID] = [(username,reward)]

    print robotID, cmdTxt, robot_command_dict
    print

    for key, val in robot_command_dict.items(): 
        if len(val)==1: del robot_command_dict[key]
        if len(val)==2 and val[0][0]==val[1][0]: del robot_command_dict[key]

    if len(robot_command_dict) != 0:
        data[(robotID, cmdTxt)] = robot_command_dict
    # print data

# true_disagreements = 0
# for key in data:
#     true_disagreements += count_disagreements(data[key])

# print "true disagreements: ", true_disagreements

# random_disgreements = []

# for i in range(0, 1000):
#     count = 0
#     for key in data:
#         temp   = shuffle_feedback( deepcopy(data[key]) )
#         count += count_disagreements(temp)
#     random_disgreements.append(count)
#     # print count

# print "random count: ", np.percentile(random_disgreements, 99)

