import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE
import numpy as np
from random import shuffle


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

sql="""SELECT displayID, count(*) as count FROM TwitchPlays.reward_log where 
reward='y' or reward='n' group by displayID having count>=2 and displayID is not NULL;"""
records = db.Execute_Select_Sql_Command(sql, ' ')

total         = 0
disagreements = 0
reward_array  = []
true_agreement_count = 0

for record in records:

    displayID = record['displayID']
    sql="""SELECT userName,reward, timeArrival FROM TwitchPlays.reward_log where 
    (reward='y' or reward='n') and displayID=%d order by timeArrival ASC;"""%(displayID)

    feedback  = db.Execute_Select_Sql_Command(sql, ' ')

    # print feedback

    userNames = set([ f['userName'] for f in feedback ])
    rewards   = [ f['reward'] for f in feedback ]
    reward_array.append( rewards )

    if len(userNames) < len(feedback): continue
    true_agreement_count += find_repeats(rewards)
    # print rewards, true_agreement_count

# print reward_array
random_agreement_count = []

for i in range(0, 1000):

    count = 0
    for rewards in reward_array:
        # shuffle(rewards)   
        rewards = ['y' if np.random.uniform(0,1)> 0.5 else 'n' for i in range(len(rewards))]   
        count += find_repeats(rewards)

    random_agreement_count.append(count)

print np.percentile(random_agreement_count, 99.99), true_agreement_count


