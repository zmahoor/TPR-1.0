''''
Author: Zahra Mahoor
Counts unique evaluations for each command and plots the most evaluated commands (top 10) along with
their counts. Note: a robot could be evaluated multiple times.
'''
import sys
import matplotlib.pyplot as plt
import numpy as np
sys.path.append('../bots')
from database import DATABASE

mydatabase = DATABASE()

sql = """select cmdTxt, count(distinct robotID) as count from display where 
        (numYes>0 or numNo>0) group by cmdTxt order by count DESC limit 10;"""

records = mydatabase.execute_select_sql_command(sql, "failed all the information.")
print records

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(records)-1, -1, -1)
y_label = [val['cmdTxt'] for val in records]
ax.barh(y_pos, [val['count'] for val in records], align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(y_label, fontsize=14)
plt.xlabel('Commands')
plt.title('Commands vs Aggregated Evaluations')
plt.grid(True)
plt.savefig('unique_evaluations_per_command.jpg', format='jpg', dpi=900)
plt.show()
