'''
Author: Zahra Mahoor
Find all the evaluations with at least two reinforcements from two different users.
Plot a heat map of disagreements for each pair command and species (command, species).
Plot disagreements/agreements for 10 original species over all the evaluations.
Plot disagreements/agreements for top commands over all the evaluations. Top: 10 commands with the most feedback.
Note: users could double vote and I remove those from the counts here.
'''

import sys
import matplotlib.pyplot as plt
import csv
import numpy as np
from collections import namedtuple, Counter
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append('../bots')
from database import DATABASE

db = DATABASE()

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot', 'quadruped':'quadruped', 'starfishbot':'starfishbot',
         'spherebot':'spherebot', 'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot',
         'snakeplusbot':'snakebot+', 'humanoid': 'humanoid', 'crabplusbot':'crabbot+', 'quadrupedplus':'quadruped+'}

sql = """SELECT d.displayID, d.cmdTxt, ro.type, count(distinct reward) as reward_count, count(distinct userName) 
        as user_count FROM TwitchPlays.display as d join TwitchPlays.reward_log as r on d.displayID=r.displayID 
       join TwitchPlays.robots  as ro on ro.robotID=d.robotID where r.reward='y' or r.reward='n' group by displayID;"""
records = db.execute_select_sql_command(sql, ' ')

robot_disagreements, command_disagreements, robot_command_disagreements = Counter(), Counter(), Counter()
robot_agreements, command_agreements, robot_command_agreements = Counter(), Counter(), Counter()

for record in records:
    rtype, cmdTxt, reward_count, user_count = record['type'], record['cmdTxt'], record['reward_count'], \
                                              record['user_count']
    if reward_count == 2 and user_count >= 1:
        robot_command_disagreements[(rtype, cmdTxt)] += 1
        command_disagreements[cmdTxt] += 1
        robot_disagreements[rtype] += 1

    elif reward_count == 1 and user_count > 1:
        robot_command_agreements[(rtype, cmdTxt)] += 1
        command_agreements[cmdTxt] += 1
        robot_agreements[rtype] += 1


robots_total = (robot_agreements + robot_disagreements)
commands_total = (command_agreements + command_disagreements)
robot_command_total = (robot_command_agreements + robot_command_disagreements)

########################################################################################################################
#write the most common (robot, command) pairs to a file
outfile = open("disagreement_data.csv", "w")
writer = csv.writer(outfile, delimiter=",")
header = ['commands']

for cmd in command_disagreements.most_common(10):
    header.append(cmd[0])
writer.writerow(header)

for robot in robot_disagreements.most_common(10):
    row = [names[robot[0]]]
    for cmd in command_disagreements.most_common(10):
        if float(robot_command_total[(robot[0], cmd[0])]) != 0:
            row.append(robot_command_disagreements[(robot[0], cmd[0])]/float(robot_command_total[(robot[0], cmd[0])]))
        else:
            print "No data: ", (robot[0], cmd[0])
            row.append(-0.0)
    writer.writerow(row)
outfile.close()

########################################################################################################################
# plot a disagreements heat map commands vs species
csv = pd.read_csv("disagreement_data.csv", index_col=0)
# print csv
fig, ax = plt.subplots(figsize=(10, 6))
heatmap = ax.pcolor(csv, cmap=plt.cm.Blues, alpha=0.8)
ax.set_frame_on(False)
ax.set_yticks(np.arange(csv.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(csv.shape[1]) + 0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
labels = list(csv.columns.values)
ax.set_xticklabels(labels, minor=False)
ax.set_yticklabels(csv.index, minor=False)
# plt.title('Disagreements (species vs commands)')
plt.xlabel('Commands (More blue = more Disagreements)')
plt.ylabel('Species')
ax.grid(False)

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
plt.savefig('disagreements_species_vs_commands.jpg', format='jpg', dpi=400)
# plt.show()
########################################################################################################################
#plot disagreements/agreements vs species
agr_list, dis_list, labels = [], [], []
for key in robot_agreements.keys():
    if key not in ('humanoid', 'crabplusbot', 'quadrupedplus', 'snakeplusbot'):
        agr_list.append(float(robot_agreements[key])/robots_total[key])
        dis_list.append(float(robot_disagreements[key])/robots_total[key])
        labels.append(names[key])

fig, ax = plt.subplots(figsize=(10, 6))
p1 = plt.bar(range(len(agr_list)), agr_list, color='b')
p2 = plt.bar(range(len(agr_list)), dis_list, color='r', bottom=agr_list)
plt.xlabel('Species')
plt.ylabel('Percentage', fontsize=14)
plt.title('Species vs. Agreements/Disagreements')
plt.xticks(np.arange(0.5, len(agr_list)+0.5, 1.0), labels)
plt.legend((p1[0], p2[0]), ('Agreements', 'Disagreements'))
plt.savefig('disagreements_species.jpg', format='jpg', dpi=400)
# plt.show()

########################################################################################################################
#plot disagreements/agreements for top 10 commands for
agr_list, dis_list, labels = [], [], []
for key, val in commands_total.most_common(10):
        agr_list.append(float(command_agreements[key])/commands_total[key])
        dis_list.append(float(command_disagreements[key])/commands_total[key])
        labels.append(key)

fig, ax = plt.subplots(figsize=(10, 6))
p1 = plt.bar(range(len(agr_list)), agr_list, color='b')
p2 = plt.bar(range(len(agr_list)), dis_list, color='r', bottom=agr_list)
plt.xlabel('Commands')
plt.ylabel('Percentage', fontsize=14)
plt.title('Commands vs. Agreements/Disagreements')
plt.xticks(np.arange(0.5, len(agr_list)+0.5, 1.0), labels)
plt.legend((p1[0], p2[0]), ('Agreements', 'Disagreements'))
plt.savefig('disagreements_commands.jpg', format='jpg', dpi=400)
# plt.show()

########################################################################################################################