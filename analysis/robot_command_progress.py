import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE
from settings import *

mydatabase = DATABASE()
Y_Vals = {}

for robot in validRobots:
	Y_Vals[robot]=[]
      
cmd   = 'stop'

fig = plt.figure()
ax  = fig.add_subplot(111)

for day in range(18, 32):

	sql = """select r.type, sum(numYes) as sumYes, sum(numNo) as sumNo from 
	display as d join robots as r on d.robotID=r.robotID where d.startTime between
	'2017-07-%d 00:00:00' and '2017-07-%d 00:00:00'+interval 1 
	day and cmdTxt='%s' group by r.type;"""%(day, day, cmd)

	records = mydatabase.execute_select_sql_command(sql, "failed all the information.")

	print records

	if records == None: continue

	for record in records:

		rtype = record['type']

	 	if record['sumYes'] == None or record['sumNo'] == None: 
	 		fitness = 0

	 	elif record['sumYes'] == 0 and record['sumNo'] == 0: 
	 		fitness = 0

	 	else:
	 		fitness = ( record['sumYes'] - record['sumNo'] ) / ( record['sumYes'] + record['sumNo'])

	 	Y_Vals[rtype].append(fitness)

print len(Y_Vals)

for robot in validRobots: 
	ax.plot(range(0, len(Y_Vals[robot])), Y_Vals[robot], '-o')

plt.legend(validRobots)

plt.title('Obedience over Time')
plt.xlabel('Day Passed')
plt.ylabel('Obedience')
plt.show()
