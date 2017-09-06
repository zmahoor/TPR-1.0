import sys
import csv
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

sql = """SELECT count(*) as count, type FROM robots where parentID!=0 group by type;"""
robots = db.Execute_Select_Sql_Command(sql, ' ')

robots = sorted(robots, key=lambda k: k['count']) 

multiple_bars = plt.figure()
ax = plt.subplot(111)

colors = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de',
	'#4393c3','#2166ac','#053061', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']

i = 0
for robot in robots:
	plt.bar(i, robot['count'], color = colors[i], label = names[robot['type']])
	i += 1
	
plt.title('Offspring Amount by Robot Type')
plt.xlabel('Type of robots')
plt.ylabel('# of offspring produced')
ax.xaxis.set_ticks([])
# ax.yaxis.set_ticks(range(0, max(l)+5, 5))
ax.yaxis.grid()
plt.legend(ncol = 2, loc=2)
plt.show()
        
        
        

