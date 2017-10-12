import sys 
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('../bots')

from database import DATABASE

mydatabase = DATABASE()

sql = """select cmdTxt, count(*) as cmdCount from TwitchPlays.command_log  group 
by cmdTxt order by cmdCount DESC LIMIT 20;"""
records = mydatabase.execute_select_sql_command(sql, "failed all the information.")

fig, ax = plt.subplots(1,1) 
y_pos   = np.arange(len(records), 0, -1)
y_label = [val['cmdTxt'] for val in records]

ax.barh(y_pos, [val['cmdCount'] for val in records], align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(y_label, fontsize=14)
# ax.invert_yaxis()  # labels read top-to-bottom

plt.xlabel('Number of Times Issued by Users')
plt.title('Top Commands Issued by Users')
plt.grid(True)

plt.show()