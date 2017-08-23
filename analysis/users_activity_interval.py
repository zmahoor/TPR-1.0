import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()
filtered = ['jfelag','zmahoor','tpr_bot2','doctorjoshuvm','twitchplaysrobotics']

for day in range(14, 15):

	fig = plt.figure()
	ax  = fig.add_subplot(111)


	print "day -------------------------------: ", day

	sql = """select min(timeArrival) as first, max(timeArrival) as last, username 
			from chats where timeArrival between
 		    2017-08-%d 10:00:00'  and '2017-08-%d 10:00:00' + interval 1 day 
 		    group by username order by first,last;"""%(day, day)

 	result   = mydatabase.Execute_Select_Sql_Command(sql , "failed all the information.")

 	if result == None: continue

 	y = 0.06

 	for record in result:

 		if record['username'] in filtered: continue

	 	interval = record['last'] - record['first']
	 	minute, seconds = divmod(interval.days*86400+interval.seconds, 60)

	 	ax.plot( [record['first'], record['last']], [y, y], '-', linewidth = 10)
	 	#legends.append(record['username'])
	 	y += 0.06

	 	print record['username'], record['first'], minute, seconds

	plt.title('Date: 2017-08-%d'%(day))
	plt.xlabel('Time')
	plt.ylabel('Users')

	plt.show()



