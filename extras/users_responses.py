import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE
import numpy as np

db = DATABASE()

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',
'quadruped':'quadruped', 'starfishbot':'starfishbot', 'spherebot':'spherebot',
'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot',
'snakeplusbot':'snakebot+', 'humanoid': 'humanoid', 'crabplusbot':'crabbot+',
'quadrupedplus':'quadruped+'}


sql="""SELECT count(*) as count, type FROM TwitchPlays.display as d join TwitchPlays.robots as r
on d.robotID=r.robotID where (numYes+numNo)>=2 group by r.type;"""
robots_total = db.execute_select_sql_command(sql, ' ')

sql="""SELECT count(*) as count, type FROM TwitchPlays.display as d join TwitchPlays.robots as r
on d.robotID=r.robotID where (numYes>=1 and numNo>=1) group by r.type;"""
robots_disagrees = db.execute_select_sql_command(sql, ' ')

prop = {}

for tot in robots_total:
    prop[names[tot['type']]] = 1.0
    for agr in robots_disagrees: 
        if tot['type'] == agr['type']: 
            prop[names[tot['type']]] = 1.0 - float(agr['count'])/tot['count']

prop = sorted(prop.iteritems(), key=lambda (k,v): (v,k)) 

print prop

agreements = [value for key, value in prop]
disagreements = [1-value for key, value in prop] 
labels = [key for key, value in prop]

p1 = plt.bar(range(len(agreements)), agreements, color='b')
p2 = plt.bar(range(len(agreements)), disagreements, color='r', bottom=agreements)

plt.ylabel('Species', fontsize=14)
plt.title('Users response vs. Species', fontsize=14)
plt.xticks(np.arange(0.5, len(agreements)+0.5, 1.0), labels, fontsize=14)
plt.legend((p1[0], p2[0]), ('agreements', 'disagreements'))
plt.show()

################################################################################
commands = ['move', 'jump', 'move forward', 'backflip', 'stop', 'spin', 'walk', 
            'roll',  'move backward', 'dance', 'run', 'flip']

sql  = "SELECT count(*) as count, cmdTxt FROM TwitchPlays.display where cmdTxt in "
sql += '('+ ",".join(["'"+k+"'" for k in commands]) + ')'
sql += " and (numYes+numNo)>=2 group by cmdTxt;"
print sql
robots_total = db.execute_select_sql_command(sql, ' ')

sql = "SELECT count(*) as count, cmdTxt FROM TwitchPlays.display where cmdTxt in "
sql += '(' + ",".join(["'"+k+"'" for k in commands]) + ')'
sql += " and (numYes>=1 and numNo>=1) group by cmdTxt;"
print sql
robots_disagrees = db.execute_select_sql_command(sql, ' ')

prop = {}

for tot in robots_total:
    prop[tot['cmdTxt']] = 1.0
    for agr in robots_disagrees: 
        if tot['cmdTxt'] == agr['cmdTxt']: 
            prop[tot['cmdTxt']] = 1.0 - float(agr['count'])/tot['count']

prop = sorted(prop.iteritems(), key=lambda (k,v): (v,k)) 
print prop

agreements = [value for key, value in prop]
disagreements = [1-value for key, value in prop] 
labels = [key for key, value in prop]

p1 = plt.bar(range(len(agreements)), agreements, color='b')
p2 = plt.bar(range(len(agreements)), disagreements, color='r', bottom=agreements)

plt.xlabel('Commands', fontsize=14)
plt.ylabel('Ratio', fontsize=14)
plt.title('Users response vs. Commands', fontsize=14)
plt.xticks(np.arange(0.5, len(agreements)+0.5, 1.0), labels, fontsize=14)
plt.legend((p1[0], p2[0]), ('agreements', 'disagreements'))
plt.show()

################################################################################
validRobots = ['1', '2', '3', '4' , 'quadruped', 'starfishbot', 'shinbot',
            'spherebot', 'snakebot', 'crabbot', 'humanoid', 'snakeplusbot', 
            'quadrupedplus', 'crabplusbot']

sql="""SELECT sum(numYes) as sumYes, sum(numNo) as sumNo, type FROM 
TwitchPlays.display as d join TwitchPlays.robots as r
on d.robotID=r.robotID group by d.robotID having (sumYes+sumNo)>=2;"""
robots = db.execute_select_sql_command(sql, ' ')

opinion = {}
for robot in validRobots: opinion[robot]=[0, 0]
agreements, disagreements, labels = [], [], []

for robot in robots:
    opinion[robot['type']][0] += 1
    if robot['sumYes'] >= 1 and robot['sumNo'] >= 1: opinion[robot['type']][1] += 1

for key in opinion.keys():
    vals = opinion[key]
    opinion[key] = float(vals[1])/vals[0]

opinion = sorted(opinion.iteritems(), key=lambda (k,v): (v,k)) 

print opinion

agreements = [value for key, value in opinion]
disagreements = [1-value for key, value in opinion] 
labels = [names[key] for key, value in opinion]

p1 = plt.bar(range(len(agreements)), agreements, color='b')
p2 = plt.bar(range(len(agreements)), disagreements, color='r', bottom=agreements)
plt.xlabel('Species')
plt.ylabel('Ratio', fontsize=14)
plt.title('Num of Robots in vs. Species')
plt.xticks(np.arange(0.5, len(agreements)+0.5, 1.0), labels)
plt.legend((p1[0], p2[0]), ('agreements', 'disagreements'))
plt.show()
################################################################################

opinion={}
for cmd in commands: opinion[cmd]=[0, 0]
agreements, disagreements, labels = [], [], []

for cmd in commands:

    sql="""SELECT sum(numYes) as sumYes, sum(numNo) as sumNo FROM 
    TwitchPlays.display where cmdTxt='%s' group by robotID having (sumYes+sumNo)>=2;"""%(cmd)
    robots = db.execute_select_sql_command(sql, ' ')

    for robot in robots:
        opinion[cmd][0] += 1
        if robot['sumYes']>=1 and robot['sumNo']>=1: opinion[cmd][1] += 1

for key in opinion.keys():
    vals = opinion[key]
    opinion[key] = 1-float(vals[1])/vals[0]

opinion = sorted(opinion.iteritems(), key=lambda (k,v): (v,k)) 

print opinion

agreements = [value for key, value in opinion]
disagreements = [1-value for key, value in opinion] 
labels = [key for key, value in opinion]

p1 = plt.bar(range(len(agreements)), agreements, color='b')
p2 = plt.bar(range(len(agreements)), disagreements, color='r', bottom=agreements)
plt.xlabel('Commands', fontsize=14)
plt.ylabel('Ratio', fontsize=14)
plt.title('Users Responses vs. Commands', fontsize=14)
plt.xticks(np.arange(0.5, len(agreements)+0.5, 1.0), labels)
plt.legend((p1[0], p2[0]), ('agreements', 'disagreements'))
plt.show()

