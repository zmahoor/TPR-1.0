import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()
filtered   = ['jfelag','zmahoor','tpr_bot2','doctorjoshuvm','twitchplaysrobotics']

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',
    'quadruped':'quadruped', 'starfishbot':'starfishbot', 'spherebot':'spherebot', 
    'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot', 
    'snakeplusbot':'snakebot+', 'humanoid': 'humanoid', 'crabplusbot':'crabbot+',
     'quadrupedplus':'quadruped+'}

sql = """select cmdTxt, count(distinct robotID) as count from display where 
        (numYes>0 or numNo>0) group by cmdTxt order by count ASC;"""

records = mydatabase.Execute_Select_Sql_Command(sql , "failed all the information.")

counts   = [value['count'] for value in  records]
commands = [value['cmdTxt'] for value in  records]

fig, ax  = plt.subplots(1,1) 
ax.plot(range(len(counts)), counts, 'o')

# Set number of ticks for x-axis
ax.set_xticks(range(len(counts)))
# Set ticks labels for x-axis
ax.set_xticklabels(commands, rotation='vertical', fontsize=10)
ax.yaxis.grid()

plt.title('Commands vs Num of Aggregated Evaluations for Critic')
plt.xlabel('Commands')
plt.ylabel('Num of Unique Samples for Critic')

plt.show()

COMMAND = 'jump'

sql = """select count(distinct d.robotID) as count, r.type from display as d join robots as r
        on d.robotID=r.robotID where d.cmdTxt='%s'
        and (d.numYes>0 or d.numNo>0) group by r.type order by count ASC;"""%(COMMAND)
        
records = mydatabase.Execute_Select_Sql_Command(sql , "failed all the information.")

print records

counts   = [value['count'] for value in  records]
Species  = [value['type'] for value in  records]

fig, ax  = plt.subplots(1,1) 
ax.plot(range(len(counts)), counts, 'o')

# Set number of ticks for x-axis
ax.set_xticks(range(len(counts)))
# Set ticks labels for x-axis
ax.set_xticklabels(Species, rotation='vertical', fontsize=10)
ax.yaxis.grid()

plt.title('Species vs Num of Aggregated Evaluations for %s'%(COMMAND))
plt.xlabel('Species')
plt.ylabel('Num of Unique Samples for Critic')

plt.show()
