import sys
import numpy as np
sys.path.append('../bots')

from database import DATABASE
import matplotlib.pyplot as plt

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',
    'quadruped':'quadruped', 'starfishbot':'starfishbot', 'spherebot':'spherebot', 
    'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot', 
    'snakeplusbot':'snakebot+', 'humanoid': 'humanoid', 'crabplusbot':'crabbot+',
     'quadrupedplus':'quadruped+'}

db = DATABASE()

sql="""SELECT type, sum(numYes) as yess, sum(numNo) as nos, sum(numLike) as likes,
sum(numDislike) as dislikes from TwitchPlays.robots as r join TwitchPlays.display as d
 on r.robotID=d.robotID group by r.type;"""
robots = db.Execute_Select_Sql_Command(sql, ' ')

sorted_robots = sorted(robots, key=lambda k: float(k['yess']-k['nos'])/float(k['yess']+k['nos'])) 

fig, ax = plt.subplots(1,1)

colors = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de',
    '#4393c3','#2166ac','#053061', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']

x = [ float(robot['yess']-robot['nos'])/float(robot['yess']+robot['nos']) for robot in sorted_robots]
y = [ float(robot['likes']-robot['dislikes'])/float(robot['likes']+robot['dislikes']) for robot in sorted_robots]
labels =[ names[robot['type']] for robot in sorted_robots]

print x, y, labels

ax.plot(x, y, 'o-', linewidth=2)
plt.title('Popularity vs. Obedience')
plt.xlabel('Obedience')
plt.ylabel('Popularity')

for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i],y[i]))

plt.show()

