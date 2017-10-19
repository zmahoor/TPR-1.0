''''
Author: Zahra Mahoor
Plot overall obedience (sum(Yes)-sum(No))/(sum(No)+sum(Yes)) for each species over time (31 days).
Subtract the obedience from the day one.
'''

import sys
import matplotlib.pyplot as plt
sys.path.append('../bots')
from database import DATABASE

mydatabase = DATABASE()

filtered = ['jfelag','zmahoor','tpr_bot2','doctorjoshuvm','twitchplaysrobotics']
mycolor = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']
validRobots = ['1', '2', '3', '4' , 'quadruped', 'starfishbot', 'shinbot',
               'spherebot', 'snakebot', 'crabbot']
names = ['stickbot', 'twigbot', 'branchbot', 'treebot', 'quadruped', 'starfishbot',
         'tablebot', 'spherebot', 'snakebot', 'crabbot']

scores, dayOne = {}, {}

for robot in validRobots:
    dayOne[robot], scores[robot] = 0, []
    for day in range(1, 31):
        sql = """SELECT (sum(numYes)-sum(numNo))/(sum(numNo)+sum(numYes)) as pro, count(*) as count 
        FROM TwitchPlays.display as d join TwitchPlays.robots as r 
        on d.robotID = r.robotID where r.type ='%s'
        and  (d.numYes!=0 or d.numNo!=0 or d.numLike!=0 or d.numDislike!=0) and
        startTime between '2017-07-18 10:00:00' and 
        '2017-07-18 10:00:00'+interval %d day;"""%(robot, day)
        record = mydatabase.execute_select_one_sql_command(sql, "failed.")

        if day == 1:
            dayOne[robot] = record['pro']
        if record['pro'] is not None:
            scores[robot].append(record['pro']-dayOne[robot])
        else:
            scores[robot].append(0)

    print robot, scores[robot]
    print

fig, ax = plt.subplots(figsize=(10, 6))
for i in range(len(validRobots)): 
    robot = validRobots[i]
    ax.plot(range(len(scores[robot])), scores[robot], 'o-', color=mycolor[i], linewidth=2)

ax.plot([0, 31],[0, 0], 'k:')
plt.legend(names, loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
plt.title('Overall Obedience over Time')
plt.xlabel('Day Passed')
plt.ylabel('Obedience')
ax.set_xticks([0, 31])
plt.savefig('../graghs/overal_obedience_over_time.jpg', format='jpg', dpi=900)
plt.show()
