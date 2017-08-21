import sys 
sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()
validRobots = ['1', '2', '3', '4' , 'quadruped', 'starfishbot', 'shinbot',
			'spherebot', 'snakebot', 'crabbot']

species = {}

for robot in validRobots: species[robot] = []

for day in range(1, 14):

	sql = """select type, count(*) as count from robots where birthDate between 
			'2017-07-18 10:00:00' and '2017-07-18 10:00:00'+ interval %d day and 
			(deathDate > '2017-07-18 10:00:00'+
		 	 interval %d day or deathDate is NULL ) group by type;"""%(day, day)

	results = mydatabase.Execute_Select_Sql_Command(sql , "failed all the information.")

	for robot in validRobots:

		found = false
		for row in results: 
			if robot == row['type']: 
				found = true 
				break

		if found:
			count  = row['count']
		else: count = 0
			
		species[rtype].append(count)

print species