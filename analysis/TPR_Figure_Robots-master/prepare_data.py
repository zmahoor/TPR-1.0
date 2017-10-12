import sys 
import csv

sys.path.append('../../bots')

from database import DATABASE

mydatabase = DATABASE()

validRobots = ['1', '2', '3', '4' , 'quadruped', 'starfishbot', 'shinbot',
			'spherebot', 'snakebot', 'crabbot']

names = {'1':'stickbot', '2': 'twigbot', '3':'branchbot', '4': 'treebot',
    'quadruped':'quadruped', 'shinbot': 'tablebot', 'crabbot': 'crabbot',
     'starfishbot':'starfishbot', 'spherebot':'spherebot', 'snakebot':'snakebot'}

species_dict = {}

header = ['species']
for i in range(1, 8): header.append(str(i))

for robot in validRobots: species_dict[robot] = [names[robot]]

for day in range(1, 8):

	sql = """select type, count(*) as count from robots where birthDate between 
			'2017-07-18 10:00:00' and '2017-07-18 10:00:00'+ interval %d day and 
			(deathDate > '2017-07-18 10:00:00'+
		 	 interval %d day or deathDate is NULL ) group by type;"""%(day, day)

	results = mydatabase.execute_select_sql_command(sql, "failed all the information.")

	print day, results
	print 

	for robot in validRobots:

		found = False
		for row in results: 
			if robot == row['type']: 
				found = True 
				break

		if found: count = str(row['count'])
		else: count = str(0)
			
		species_dict[robot].append(count)


with open("data.csv", "w") as outfile:

	writer = csv.writer(outfile, delimiter=",")
	writer.writerow(header)

	for robot in validRobots:
		writer.writerow(species_dict[robot])


print 
print
print species_dict