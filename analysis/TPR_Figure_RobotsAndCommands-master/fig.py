import matplotlib.pyplot as plt
import pandas as pd
from urllib2 import urlopen
import numpy as np

csv = pd.read_csv("data.csv", index_col=0)
#print csv

csv_sort = csv.sort_values('total', axis=1, ascending=False)
#print csv_sort

fig, ax = plt.subplots()
heatmap = ax.pcolor(csv_sort, cmap=plt.cm.Blues, alpha=0.8)

fig = plt.gcf()
fig.set_size_inches(8, 11)

ax.set_frame_on(False)

ax.set_yticks(np.arange(csv_sort.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(csv_sort.shape[1]) + 0.5, minor=False)

ax.invert_yaxis()
ax.xaxis.tick_top()

labels = list(csv_sort.columns.values)
#print labels
#labels = ['1234','437','228','214']

#labels = ['Games', 'Minutes', 'Points', 'Field goals made', 'Field goal attempts', 'Field goal percentage', 'Free throws made', 'Free throws attempts', 'Free throws percentage', 'Three-pointers made', 'Three-point attempt', 'Three-point percentage', 'Offensive rebounds', 'Defensive rebounds', 'Total rebounds', 'Assists', 'Steals', 'Blocks', 'Turnover', 'Personal foul']

ax.set_xticklabels(labels, minor=False)
ax.set_yticklabels(csv_sort.index, minor=False)

plt.xticks(rotation=90)

plt.title('More blue = more obedient\n\n\n')
plt.xlabel('Robots')
plt.ylabel('Commands')

ax.grid(False)

ax = plt.gca()

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False

plt.show()
