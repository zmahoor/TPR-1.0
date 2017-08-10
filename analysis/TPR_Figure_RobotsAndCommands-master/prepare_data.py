import sys
import csv

sys.path.append('../bots')

from database import DATABASE

db = DATABASE()

topn_robots = 7
topn_cmds   = 7

sql    = """SELECT * FROM robots order by totalFitness DESC limit %d;"""%(topn_robots)
robots = db.Execute_Select_Sql_Command(sql, err_msg="Failed executing the select.")

# print robots

totalFitness = [robot['totalFitness'] for robot in robots]

print totalFitness

stats      = open("output.csv",'w') 
csv_writer = csv.writer(stats, dialect='excel')
csv_writer.writerow(totalFitness)

sql  = "SELECT cmdTxt, totalLearnability FROM unique_commands order by totalLearnability DESC limit %d;"%(topn_cmds)
top_commands = db.Execute_Select_Sql_Command(sql, err_msg="Failed executing the select.")

print top_commands
print 

for command in top_commands:

	cmdTxt      = command['cmdTxt']
	fitnessList = []

	for robot in robots:

		robotID = robot['robotID']

		print robotID, cmdTxt

		sql = """SELECT cmdTxt, sum(numYes)-sum(numNo) as fitness FROM display where robotID=%d and cmdTxt='%s';"""%(robotID, cmdTxt)

		command_fitness = db.Execute_SelectOne_Sql_Command(sql, err_msg="Failed executing the select.")
		fitnessList.append(command_fitness['fitness'])

	print fitnessList
	
	csv_writer.writerow(fitnessList)

stats.close()