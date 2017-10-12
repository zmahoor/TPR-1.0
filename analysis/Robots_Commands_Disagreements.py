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

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',
    'quadruped':'quadruped', 'starfishbot':'starfishbot', 'spherebot':'spherebot', 
    'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot', 
    'snakeplusbot':'snakebot+', 'humanoid': 'humanoid', 'crabplusbot':'crabbot+',
     'quadrupedplus':'quadruped+'}

sql="""SELECT d.displayID, d.robotID, userName, reward, r.timeArrival, d.cmdTxt, ro.type
FROM TwitchPlays.display as d join TwitchPlays.reward_log as r on d.displayID=r.displayID 
join TwitchPlays.robots  as ro on ro.robotID=d.robotID where r.reward='y' or r.reward='n'
order by r.timeArrival ASC;"""
records = db.execute_select_sql_command(sql, ' ')

displays_dict, command_robot = {}, {}
robot_disagreements, command_disagreements, robot_command_disagreements = Counter(), Counter(), Counter()
robot_agreements, command_agreements, robot_command_agreements = Counter(), Counter(), Counter()
num_disagreements, num_agreements = 0, 0

for record in records:
    displayID, userName, reward = record['displayID'], record['userName'], record['reward']
    command_robot[displayID] = (record['type'], record['cmdTxt'])

    if displayID not in displays_dict: displays_dict[displayID] = set()
    displays_dict[displayID].add((userName, reward))

#delete all the evaluations with only one feedback
for key, val in displays_dict.items(): 
    if len(val) == 1: del displays_dict[key]

# iterate over the rest and find the total number of agreements, total number of disagreements
# agreements/disagreements per robot/command
for key, val in displays_dict.items(): 
    feedback = set([v[1] for v in val])
    robot, command = command_robot[key]

    if len(feedback) == 2: 
        num_disagreements += 1
        robot_disagreements[robot] += 1
        command_disagreements[command] += 1
        robot_command_disagreements[(robot, command)] += 1

    else:
        num_agreements += 1
        robot_agreements[robot] += 1
        command_agreements[command] += 1
        robot_command_agreements[(robot, command)] += 1

print "Total displays with agreements: {}.".format(num_agreements)
print "Total displays with disagreements: {}.".format(num_disagreements)

#calcuate the total number of evaluations with at least two feedback
#1) for each species
#2) for each command
#3) for pair of (robot, command)
robots_total = (robot_agreements + robot_disagreements)
commands_total = (command_agreements + command_disagreements)
robot_command_total = (robot_command_agreements + robot_command_disagreements)

#write the most common robot command pairs to a file for a heat map
outfile = open("disagreement_data.csv", "w")
writer = csv.writer(outfile, delimiter=",")
header = ['commands']

for cmd in command_disagreements.most_common(10): header.append(cmd[0])
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
# plot a heat map
csv = pd.read_csv("disagreement_data.csv", index_col=0)
print csv
fig, ax  = plt.subplots()
heatmap  = ax.pcolor(csv, cmap=plt.cm.Blues, alpha=0.8)
fig = plt.gcf()
fig.set_size_inches(9, 11)

ax.set_frame_on(False)
ax.set_yticks(np.arange(csv.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(csv.shape[1]) + 0.5, minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
labels = list(csv.columns.values)
ax.set_xticklabels(labels, minor=False)
ax.set_yticklabels(csv.index, minor=False)

# plt.xticks(rotation=90)

# plt.title('More blue = more obedient\n\n\n')
plt.xlabel('Commands (More blue = more Disagreements)')
plt.ylabel('Species')
ax.grid(False)
ax = plt.gca()

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False

plt.show()
########################################################################################################################

#write the most common robot command pairs to a file for a heat map
# outfile = open("agreement_data.csv", "w")
# writer  = csv.writer(outfile, delimiter=",")
# header = ['commands']
#
# for cmd in command_agreements.most_common(10): header.append(cmd[0])
# writer.writerow(header)
#
# for robot in robot_agreements.most_common(10):
#     row = [names[robot[0]]]
#     for cmd in command_agreements.most_common(10):
#         if float(robot_command_total[(robot[0], cmd[0])]) != 0:
#             row.append(robot_command_agreements[(robot[0], cmd[0])]/float(robot_command_total[(robot[0], cmd[0])]))
#         else:
#             print "No data: ", (robot[0], cmd[0])
#             row.append(-0.0)
#     writer.writerow(row)
#
# outfile.close()
#
# ########################################################################################################################
# # plot a heat map
# csv = pd.read_csv("agreement_data.csv", index_col=0)
# print csv
# fig, ax  = plt.subplots()
# heatmap  = ax.pcolor(csv, cmap=plt.cm.Blues, alpha=0.8)
# fig = plt.gcf()
# fig.set_size_inches(9, 11)
#
# ax.set_frame_on(False)
# ax.set_yticks(np.arange(csv.shape[0]) + 0.5, minor=False)
# ax.set_xticks(np.arange(csv.shape[1]) + 0.5, minor=False)
# ax.invert_yaxis()
# ax.xaxis.tick_top()
# labels = list(csv.columns.values)
# ax.set_xticklabels(labels, minor=False)
# ax.set_yticklabels(csv.index, minor=False)
#
# # plt.xticks(rotation=90)
#
# plt.xlabel('Commands (More blue = more Agreements)')
# plt.ylabel('Species')
# ax.grid(False)
# ax = plt.gca()
#
# for t in ax.xaxis.get_major_ticks():
#     t.tick1On = False
#     t.tick2On = False
# for t in ax.yaxis.get_major_ticks():
#     t.tick1On = False
#     t.tick2On = False
#
# plt.show()
########################################################################################################################

# print
# print robot_agreements
# print robot_disagreements
# print robots_total
#
# agr_list, dis_list, labels = [], [], []
#
# for key in robot_agreements.keys():
#     if key not in ('humanoid', 'crabplusbot', 'quadrupedplus', 'snakeplusbot'):
#         agr_list.append(float(robot_agreements[key])/robots_total[key])
#         dis_list.append(float(robot_disagreements[key])/robots_total[key])
#         labels.append(names[key])
#
# p1 = plt.bar(range(len(agr_list)), agr_list, color='b')
# p2 = plt.bar(range(len(agr_list)), dis_list, color='r', bottom=agr_list)
# plt.xlabel('Species')
# plt.ylabel('Ratio', fontsize=14)
# plt.title('Species vs. Agreements/Disagreements')
# plt.xticks(np.arange(0.5, len(agr_list)+0.5, 1.0), labels)
# plt.legend((p1[0], p2[0]), ('Agreements', 'Disagreements'))
# plt.show()