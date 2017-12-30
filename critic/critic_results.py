import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import misc
from scipy.stats.stats import ttest_ind

filename1 = 'critic_results_regular_1f'
filename2 = 'critic_results_permuted_1f'


def stars(p, m=16):
    p *= 22
    # p *= misc.comb(m, 2)  # with Bonferroni adjustment for multiple comparisons
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "n.s."


regular = pd.read_csv("/Users/twitchplaysrobotics/TPR-1.0/critic/"+filename1+".csv", index_col=0).transpose()
permuted = pd.read_csv("/Users/twitchplaysrobotics/TPR-1.0/critic/"+filename2+".csv", index_col=0).transpose()

regular_mean, regular_std = regular.mean(), regular.std()
regular_std = 2.575*(regular_std/(30**0.5))  # 99% CI bounds
permuted_mean, permuted_std = permuted.mean(), permuted.std()
permuted_std = 2.575*(permuted_std/(30**0.5))
regular_permuted_p_value = ttest_ind(regular, permuted, equal_var=False)

fig, ax = plt.subplots(figsize=(8, 6))

x = []
for _ in range(len(regular.columns)):
    x.append(x[-1] + 0.25 if len(x) > 0 else 0.15)
    x.append(x[-1] + 0.05)

# print x
points, x_ticks, i = [None]*2*len(regular.columns), [], 0

for key in regular:
    points[i] = ax.errorbar(x[i+1], regular_mean[key], yerr=regular_std[key], fmt='o', markersize=5, color='g',
                            elinewidth=2, capsize=4, ecolor='g')
    points[i+1] = ax.errorbar(x[i], permuted_mean[key], yerr=permuted_std[key], fmt='o', markersize=5, color='r',
                              elinewidth=2, capsize=4, ecolor='r')
    x_ticks.extend([key, ""])
    y_max = max(regular_mean[key]+regular_std[key], permuted_mean[key]+permuted_std[key])

    ax.annotate("", xy=(x[i], y_max), xycoords='data', xytext=(x[i+1], y_max), textcoords='data',
                arrowprops=dict(arrowstyle="-", connectionstyle="bar,fraction=0.3"))

    # print key, ttest_ind(regular[key], permuted[key], equal_var=False)

    ax.text(x[i]+0.02, y_max+.02, stars(ttest_ind(regular[key], permuted[key], equal_var=False)[1]),
            horizontalalignment='center', verticalalignment='center')
    i += 2


i = 0
best_one = 'tablebot'
for key in regular:

   if key == best_one:
       continue

   print key, ttest_ind(regular[key], regular[best_one], equal_var=False)[1]*misc.comb(16, 2), \
       stars(ttest_ind(regular[key], regular[best_one], equal_var=False)[1])

ax.set_ylabel("Mean Absolute Error")
ax.set_xticks(x,)
ax.set_xticklabels(x_ticks, rotation=0)
ax.set_title("Mean Error of Predictive Model Across 30 Trials for each Species")
ax.legend((points[0], points[1]), ("Experiment", "Permuted Control"), loc=0,  numpoints=1, fontsize=14)
plt.xlim((x[0] - .1, x[len(x) - 1] + .1))
plt.ylim((.05, .7))
plt.savefig(filename1+'.jpg', format='jpg', dpi=900)
plt.show()
