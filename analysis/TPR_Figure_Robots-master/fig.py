import matplotlib.pyplot as plt
import pandas as pd
from urllib2 import urlopen
import numpy as np

csv = pd.read_csv("data.csv", index_col=0)
csv = csv.transpose()

mycolor = ['#67001f','#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac','#053061']

csv.plot.bar(stacked=True, figsize=(12, 8), color=mycolor)
plt.title('Number of robots in each species', fontsize=20)
plt.xlabel('Day', fontsize=18)
plt.ylabel('Population size', fontsize=18)
plt.legend(loc='center left', bbox_to_anchor=(1,0.5), ncol=1)

plt.show()
