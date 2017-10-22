''''
Author: Zahra Mahoor
Plot obedience vs popularity for every robots of different species.
obedience = (Yes - No)/(Yes + No)
Popularity = (Like - Dislike)/(Like + Dislike)
'''

import sys
import numpy as np
import seaborn as sns
sns.set(color_codes=True)
sys.path.append('../bots')
from database import DATABASE
import matplotlib.pyplot as plt

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',
        'quadruped':'quadruped', 'starfishbot':'starfishbot', 'spherebot':'spherebot',
        'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot',
        'snakeplusbot':'snakebot+', 'humanoid': 'humanoid', 'crabplusbot':'crabbot+',
         'quadrupedplus':'quadruped+'}

db = DATABASE()

# sql="""SELECT type, sum(numYes) as yess, sum(numNo) as nos, sum(numLike) as likes,
# sum(numDislike) as dislikes from TwitchPlays.robots as r join TwitchPlays.display as d
#  on r.robotID=d.robotID group by r.type;"""
# robots = db.Execute_Select_Sql_Command(sql, ' ')
#
# x = [ robot['yess']-robot['nos'] for robot in robots ]
# y = [ robot['likes']-robot['dislikes'] for robot in robots ]
# labels = [ names[robot['type']] for robot in robots ]
#
# print x, y, labels
#
# fig, ax = plt.subplots(1,1)
# ax.plot(x, y, 'o')
# plt.axhline(0, color='r', linestyle='--', linewidth=4)
# plt.axvline(0, color='r', linestyle='--', linewidth=4)
# plt.title('Popularity vs. Obedience', fontsize=14)
# plt.xlabel('Obedience (Total Yes\'s - Total No\'s)', fontsize=14)
# plt.ylabel('Popularity (Total Likes - Total Dislikes)', fontsize=14)
# for i, txt in enumerate(labels):
#     ax.annotate(txt, (x[i],y[i]), fontsize=14)
#
# plt.show()
#
# ################################################################################
#
# progress_in_obedience = {}
# progress_in_popularity= {}
#
# sql = """ SELECT type, min(startTime) as firstTime, max(startTime) as lastTime
#     from TwitchPlays.robots as r join TwitchPlays.display as d
#     on r.robotID=d.robotID group by r.type;"""
#
# records = db.Execute_Select_Sql_Command(sql, "Faild to fetch")
# if records == None: exit()
#
# for row in records:
#     # print row
#     robot_type = row['type']
#     start_time, last_time = row['firstTime'], row['lastTime']
#
#     first_half_obedience, second_half_obedience = 0, 0
#     first_half_popularity, second_half_popularity = 0, 0
#
#     mid_time   = start_time + (last_time - start_time)/2
#     # print mid_time
#
#     sql = """SELECT type,(sum(numYes)-sum(numNo)) as obedience,count(d.displayID) as nevals,
#     (sum(numLike)-sum(numDislike)) as popularity FROM TwitchPlays.robots as r join
#     TwitchPlays.display as d on r.robotID=d.robotID WHERE
#     startTime <= '%s' and type='%s';"""%(mid_time, robot_type)
#
#     result = db.Execute_SelectOne_Sql_Command(sql, "Faild to fetch")
#
#     # print result
#
#     if result['type'] != None:
#         first_half_obedience = float(result['obedience'])/result['nevals']
#         first_half_popularity = float(result['popularity'])/result['nevals']
#
#     sql = """SELECT type,(sum(numYes)-sum(numNo)) as obedience,count(d.displayID)
#     as nevals,(sum(numLike)-sum(numDislike)) as popularity  FROM TwitchPlays.robots
#     as r join TwitchPlays.display as d on r.robotID=d.robotID WHERE
#     startTime>'%s' and type='%s';"""%(mid_time, robot_type)
#
#     result = db.Execute_SelectOne_Sql_Command(sql, "Failed to fetch")
#
#     if result['type'] != None:
#         second_half_obedience = float(result['obedience'])/result['nevals']
#         second_half_popularity = float(result['popularity'])/result['nevals']
#
#     progress_in_obedience[robot_type]  = second_half_obedience - first_half_obedience
#     progress_in_popularity[robot_type] = second_half_popularity - first_half_popularity
#
#     # print result
# # print
# print progress_in_obedience
# print
# print progress_in_popularity
#
# x = [ progress_in_obedience[n] for n in names.keys() ]
# y = [ progress_in_popularity[n] for n in names.keys() ]
# labels = [ names[n] for n in names.keys() ]
#
# print
# print x, y, labels
#
# fig, ax = plt.subplots(1,1)
# ax.plot(x, y, 'o')
# plt.axhline(0, color='r', linestyle='--', linewidth=4)
# plt.axvline(0, color='r', linestyle='--', linewidth=4)
# plt.title('Porgress in Popularity vs. Progress in Obedience', fontsize=14)
# plt.xlabel('Progress in Obedience', fontsize=14)
# plt.ylabel('Progress in Popularity', fontsize=14)
# for i, txt in enumerate(labels):
#     ax.annotate(txt, (x[i],y[i]), fontsize=14)
#
# plt.show()

########################################################################################################################

for key, val in names.items():
    sql = """select * from robots where type='%s'"""%key
    result = db.execute_select_sql_command(sql, "Failed to fetch")

    x = np.array([(r['sumYes']-r['sumNo'])/float(r['sumYes']+r['sumNo']) if (r['sumYes']+r['sumNo']) > 0
                  else 0 for r in result])
    y = np.array([(r['sumLike']-r['sumDislike'])/float(r['sumLike']+r['sumDislike']) if
                  (r['sumLike']+r['sumDislike']) > 0 else 0 for r in result])
    sns.plt.figure()
    ax = sns.regplot(x=x, y=y, color="g")
    ax.set(xlabel="Obedience", ylabel="Popularity")
    ax.set_title('Popularity vs. Obedience of %s'%val)
    sns.plt.savefig(key+'_obedience_vs_popularity.png', dpi=900)
