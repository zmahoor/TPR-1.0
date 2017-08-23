import sys 
import matplotlib.pyplot as plt

sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()
filtered = ['jfelag','zmahoor','tpr_bot2','doctorjoshuvm','twitchplaysrobotics']

sql = """select cmdTxt, count(*) as count from display where (numYes>0 or numNo>0) 
        group by cmdTxt order by count ASC;"""
records = mydatabase.Execute_Select_Sql_Command(sql , "failed all the information.")

counts = [value['count'] for value in  records]
commands = [value['cmdTxt'] for value in  records]

fig, ax = plt.subplots(1,1) 
ax.plot(range(len(counts)), counts, 'o')

# Set number of ticks for x-axis
ax.set_xticks(range(len(counts)))
# Set ticks labels for x-axis
ax.set_xticklabels(commands, rotation='vertical', fontsize=10)

plt.title('Commands vs #Reinforcements')
plt.xlabel('Commands')
plt.ylabel('Num of Reinforcements')

plt.show()
