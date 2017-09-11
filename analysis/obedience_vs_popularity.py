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

# sorted_robots = sorted(robots, key=lambda k: float(k['yess']-k['nos'])/float(k['yess']+k['nos'])) 

fig, ax = plt.subplots(1,1)

colors = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de',
    '#4393c3','#2166ac','#053061', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']

# x = [ float(robot['yess']-robot['nos'])/float(robot['yess']+robot['nos']) for robot in sorted_robots]
# y = [ float(robot['likes']-robot['dislikes'])/float(robot['likes']+robot['dislikes']) for robot in sorted_robots]

x = [ robot['yess']-robot['nos'] for robot in robots ]
y = [ robot['likes']-robot['dislikes'] for robot in robots ]

labels = [ names[robot['type']] for robot in robots]

print x, y, labels

ax.plot(x, y, 'o')
plt.axhline(0, color='r', linestyle='--', linewidth=4)
plt.axvline(0, color='r', linestyle='--', linewidth=4)
plt.title('Popularity vs. Obedience', fontsize=14)
plt.xlabel('Obedience (Total Yes\'s - Total No\'s)', fontsize=14)
plt.ylabel('Popularity (Total Likes - Total Dislikes)', fontsize=14)

for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i],y[i]), fontsize=14)

plt.show()

################################################################################
        sql = """ SELECT cmdTxt, min(startTime) as firstTime, max(startTime) as lastTime
            from TwitchPlays.robots as r join TwitchPlays.display as d
            on r.robotID=d.robotID group by r.type;"""
            
        err_msg = "Faild to fetch command names..."
        records = self.Execute_Select_Sql_Command(sql, err_msg)

        if records == None: return

        for row in records:
            # print row
            command    = row['cmdTxt']
            start_time = row['firstTime']
            last_time  = row['lastTime']
            first_sum  = 0
            second_sum = 0
            mid_time   = start_time + (last_time - start_time)/2
            # print mid_time

            sql = """SELECT cmdTxt, (sum(numYes)-sum(numNo)) as firstSum FROM 
                    display WHERE startTime <= '%s' and cmdTxt='%s';"""%(mid_time, command)
            err_msg = "Faild to fetch command names"
            result = self.Execute_SelectOne_Sql_Command(sql, err_msg)

            # print result

            if result['cmdTxt'] != None: 
                first_sum = result['firstSum']

            sql = """SELECT cmdTxt, (sum(numYes)-sum(numNo)) as secondSum FROM
             display WHERE startTime > '%s' and cmdTxt='%s';"""%(mid_time, command)

            result = self.Execute_SelectOne_Sql_Command(sql)
            # print result



