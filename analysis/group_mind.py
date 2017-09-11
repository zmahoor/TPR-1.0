import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE
import numpy as np

db = DATABASE()

sql="""SELECT displayID, count(*) as count FROM TwitchPlays.reward_log where 
reward='y' or reward='n' group by displayID having count=2 and displayID is not NULL;"""
records = db.Execute_Select_Sql_Command(sql, ' ')

total         = 0
disagreements = 0
total_array   = []
double_vote   = 0
disagreements_with_yourself = 0

for record in records:

    displayID = record['displayID']
    sql="""SELECT userName,reward FROM TwitchPlays.reward_log where 
    (reward='y' or reward='n') and displayID=%d;"""%(displayID)

    feedback  = db.Execute_Select_Sql_Command(sql, ' ')

    if feedback[0]['userName'] == feedback[1]['userName']: 
        double_vote += 1

        if feedback[0]['reward'] != feedback[1]['reward']: 
            disagreements_with_yourself += 1

    if feedback[0]['userName'] != feedback[1]['userName']:
        total += 1
        total_array.append([int(feedback[0]['reward']=='y'), int(feedback[1]['reward']=='y')])

        if feedback[0]['reward'] != feedback[1]['reward']: 
            disagreements += 1

print len(records), double_vote, disagreements_with_yourself, total, disagreements, float(disagreements)/total

print np.array(total_array)
################################################################################
