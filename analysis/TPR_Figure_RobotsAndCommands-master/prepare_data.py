import sys
import csv
import numpy as np
sys.path.append('../../bots')

from database import DATABASE

db = DATABASE()

outfile = open("data.csv", "w")
writer  = csv.writer(outfile, delimiter=",")

validRobots = ['1', '2', '3', '4' , 'quadruped', 'starfishbot', 'shinbot',
			'spherebot', 'snakebot', 'crabbot']

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',
    'quadruped':'quadruped', 'starfishbot':'starfishbot', 'spherebot':'spherebot', 
    'shinbot': 'tablebot', 'snakebot':'snakebot', 'crabbot': 'crabbot',}

commands = ['move', 'jump', 'move forward', 'backflip', 'stop', 'spin', 'walk', 
			'roll',  'move backward', 'dance', 'run', 'flip']

header = ['species']
for i in range(0, len(validRobots)):
	robot = validRobots[i]
	header.append(names[robot])

print header
writer.writerow(header)

score_matrix = np.zeros((len(commands)+2, len(validRobots)))

MIN = -1
MAX = 1

for i in range( len(commands)+2 ):

	if i == 0: 
		command = 'total'
		row  = ['total']

	elif i == len(commands)+1:
		command = 'others'
		row  = ['others']

	else:
		command = commands[i-1]
		row = [command]

	for j in range(len(validRobots)):
		robot = validRobots[j]

		if i == 0:
			sql = """SELECT sum(numYes) as sumYes, sum(numNo) as sumNo 
			FROM display as d join robots as r on d.robotID=r.robotID
			where r.type='%s';"""%(robot)


		elif i == len(commands)+1:
			sql = """SELECT sum(numYes) as sumYes, sum(numNo) as sumNo 
			FROM display as d join robots as r on d.robotID=r.robotID
			where r.type='%s' and cmdTxt not in """%(robot)

			sql +=  '('+ ",".join(["'"+k+"'" for k in commands]) + ');'

		else:
			sql = """SELECT cmdTxt, sum(numYes) as sumYes, sum(numNo) as sumNo 
			FROM display as d join robots as r on d.robotID=r.robotID
			where r.type='%s' and cmdTxt='%s';"""%(robot, command)

		results = db.Execute_SelectOne_Sql_Command(sql, 
				 err_msg="Failed executing the select.")

		obedience = (results['sumYes']-results['sumNo'])/(results['sumYes']+results['sumNo'])
		score_matrix[i][j] = obedience = (obedience - MIN) / (MAX-MIN)
		row.append(str(obedience))

	writer.writerow(row)
	print command, row, '\n'

outfile.close()


