import sys
import csv

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

score_list = ['total']

for i in range(0, len(validRobots)):
	robot = validRobots[i]

	sql = """SELECT sum(numYes) as sumYes, sum(numNo) as sumNo 
		FROM display as d join robots as r on d.robotID=r.robotID
		where r.type='%s';"""%(robot)

	total_fitness = db.Execute_SelectOne_Sql_Command(sql, 
						err_msg="Failed executing the select.")

	obedience = (total_fitness['sumYes'] - total_fitness['sumNo'])

	# obedience = (total_fitness['sumYes'] - total_fitness['sumNo'])/(total_fitness['sumYes'] + total_fitness['sumNo'])
	score_list.append(str(obedience))

print score_list
writer.writerow(score_list)

# for each default command
for command in commands:

	score_list  = [command]

	for i in range(0, len(validRobots)):
		robot = validRobots[i]

		sql = """SELECT cmdTxt, sum(numYes) as sumYes, sum(numNo) as sumNo 
			FROM display as d join robots as r on d.robotID=r.robotID
			where r.type='%s' and cmdTxt='%s';"""%(robot, command)

		cmd_fitness = db.Execute_SelectOne_Sql_Command(sql, 
							err_msg="Failed executing the select.")

		obedience = (cmd_fitness['sumYes'] - total_fitness['sumNo'])
		# obedience = (cmd_fitness['sumYes'] - total_fitness['sumNo'])/(cmd_fitness['sumYes'] + cmd_fitness['sumNo'])
		score_list.append(str(obedience))

	print command, score_list
	print

	writer.writerow(score_list)


outfile.close()


