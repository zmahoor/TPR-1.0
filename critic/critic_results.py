import sys
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats.stats import ttest_ind

filename1 = 'critic_results_regular'
filename2 = 'critic_results_permuted'


def stars(p):
   if p < 0.0001:
       return "****"
   elif p < 0.001:
       return "***"
   elif p < 0.01:
       return "**"
   elif p < 0.05:
       return "*"
   else:
       return "-"


regular = pd.read_csv("/Users/zahra/TPR-1.0/critic/"+filename1+".csv", index_col=0).transpose()
permuted = pd.read_csv("/Users/zahra/TPR-1.0/critic/"+filename2+".csv", index_col=0).transpose()

regular_mean, regular_std = regular.mean(), regular.std()
permuted_mean, permuted_std = permuted.mean(), permuted.std()

print permuted
print permuted_mean
print permuted_std

regular_permuted_p_value = ttest_ind(regular, permuted)

fig, ax = plt.subplots(figsize=(8,6))

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
    ax.text(x[i]+0.02, y_max+.01, stars(ttest_ind(regular[key], permuted[key])[1]*2), horizontalalignment='center',
            verticalalignment='center')
    i += 2

ax.set_ylabel("Mean Absolute Error")
ax.set_xticks(x)
ax.set_xticklabels(x_ticks)
ax.set_title("Mean Error of Predictive Model Across 30 Trials for each Species")
ax.legend((points[0], points[1]), ("Experiment", "Permuted Control"), loc=0,  numpoints=1, fontsize=14)
plt.xlim((x[0] - .1, x[len(x) - 1] + .1))
plt.ylim((.05, .7))
plt.savefig(filename1+'.eps', format='eps', dpi=900)
# plt.show()
