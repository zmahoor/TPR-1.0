''''
Author: Zahra Mahoor
Counts all commands typed by users and plots the most issued commands (top 20) along with
their counts.
'''
import sys
import matplotlib.pyplot as plt
import numpy as np
sys.path.append('../bots')
from database import DATABASE

mydatabase = DATABASE()

sql = """select cmdTxt, count(*) as cmdCount from TwitchPlays.command_log  group 
         by cmdTxt order by cmdCount DESC LIMIT 20;"""
records = mydatabase.execute_select_sql_command(sql, "failed all the information.")

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(records)-1, -1, -1)
y_label = [val['cmdTxt'] for val in records]
ax.barh(y_pos, [val['cmdCount'] for val in records], align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(y_label, fontsize=14)
plt.xlabel('Number of Times Issued by Users')
plt.title('Top Issued Commands by Users')
plt.grid(True)
plt.savefig('../graphs/count_issued_commands.jpg', format='jpg', dpi=900)
plt.show()