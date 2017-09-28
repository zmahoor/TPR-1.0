import sys 
import matplotlib.pyplot as plt

command = 'move'

# regular_data = {'starfishbot':[0.151, 0.035], 'branchbot':[0.286, 0.091]}
# permuted_data = {'starfishbot':[0.242, 0.088], 'branchbot':[0.384, 0.091]}
# random_model = {'starfishbot':[0.817, 0.082], 'branchbot':[0.459, 0.110]}
#
# fig, ax = plt.subplots()
#
# x = [.15, .25, .35, .55, .65, .75]
#
# point0 = ax.errorbar(x[2], regular_data['starfishbot'][0],
#             yerr = regular_data['starfishbot'][1],
#             fmt = 'o', markersize = 5, color = 'g', ecolor = 'g')
# point1 = ax.errorbar(x[1], permuted_data['starfishbot'][0],
#             yerr = permuted_data['starfishbot'][1],
#             fmt = 'o', markersize = 5, color = 'r', ecolor = 'r')
# point2 = ax.errorbar(x[0], random_model['starfishbot'][0],
#             yerr = random_model['starfishbot'][1],
#             fmt = 'o', markersize = 5, color = 'b', ecolor = 'b')
#
# point3 = ax.errorbar(x[5], regular_data['branchbot'][0],
#             yerr = regular_data['branchbot'][1],
#             fmt = 'o', markersize = 5, color = 'g', ecolor = 'g')
# point4 = ax.errorbar(x[4], permuted_data['branchbot'][0],
#             yerr = permuted_data['branchbot'][1],
#             fmt = 'o', markersize = 5, color = 'r', ecolor = 'r')
# point5 = ax.errorbar(x[3], random_model['branchbot'][0],
#             yerr = random_model['branchbot'][1],
#             fmt = 'o', markersize = 5, color = 'b', ecolor = 'b')
#
# ax.set_ylabel("Error")
# ax.set_xticks(x)
# ax.set_xticklabels(["", "Starfishbot", "", "", "Branchbot", ""])
# ax.set_title("Mean Error of Predictive Model")
# ax.legend((point0[0], point1[0], point2[0]), ("Experiment", "Permuted\nControl", "Random\nControl"),
#         loc = 9,  numpoints = 1, fontsize = 10)
# plt.xlim((x[0] - .1, x[len(x) -1] + .1))
# plt.ylim((.395, .53))

# plt.show()
########################################################################################################################


def stars(p):
   if p < 0.0001:
       return "****"
   elif (p < 0.001):
       return "***"
   elif (p < 0.01):
       return "**"
   elif (p < 0.05):
       return "*"
   else:
       return "-"

# command = ['move', 'stop']
regular_data = {'starfishbot':[0.197, 0.043], 'branchbot':[0.350, 0.074], 'snakebot':[0.387, 0.043], 'tablebot':[0.212, 0.073],
               'quadruped':[0.396, 0.062], 'treebot':[0.292, 0.066], 'spherebot':[0.411, 0.057], 'stickbot':[0.419, 0.063],
                'twigbot':[0.370, 0.107]}
permuted_data = {'starfishbot':[0.491, 0.065], 'branchbot':[0.470, 0.083], 'snakebot':[0.488, 0.037], 'tablebot':[0.478, 0.097],
                'quadruped':[0.474, 0.065], 'treebot':[0.452, 0.104], 'spherebot':[0.486, 0.069], 'stickbot':[0.488, 0.088],
                'twigbot':[0.494, 0.105]}
# random_model = {'starfishbot':[0.5, 0.059], 'branchbot':[0.538, 0.148], 'snakebot':[0.482, 0.077], 'tablebot':[0.490, 0.094],
#                 'quadruped':[0.428, 0.133], 'treebot':[], 'spherebot':[]}

regular_permuted_p_value = {'starfishbot': 5.3238905170342945e-28, 'branchbot':3.0461481443595506e-07, 'snakebot':1.4964029414300558e-13,
                            'tablebot':4.466754369482279e-17, 'quadruped':1.6739299729529018e-05, 'treebot': 2.9136521042000613e-09,
                            'spherebot':2.7774022198088076e-05, 'stickbot':0.0010708904740438063, 'twigbot':4.166608497071619e-05}

fig, ax = plt.subplots()

x = []
for _ in range(len(regular_data)):
    x.append(x[-1] + 0.25 if len(x) > 0 else 0.15)
    x.append(x[-1] + 0.05)

# print x
points, x_ticks, i = [None]*2*len(regular_data), [], 0

for key in regular_data.iterkeys():
    points[i] = ax.errorbar(x[i+1], regular_data[key][0], yerr=regular_data[key][1], fmt='o', markersize=5, color='g',
                            elinewidth=2, capsize=4, ecolor='g')
    points[i+1] = ax.errorbar(x[i], permuted_data[key][0], yerr=permuted_data[key][1], fmt='o', markersize=5, color='r',
                              elinewidth=2, capsize=4, ecolor='r')
    x_ticks.extend([key, ""])
    y_max = max(regular_data[key][0]+regular_data[key][1], permuted_data[key][0]+permuted_data[key][1])

    ax.annotate("", xy=(x[i], y_max), xycoords='data', xytext=(x[i+1], y_max), textcoords='data',
                arrowprops=dict(arrowstyle="-", ec='#aaaaaa', connectionstyle="bar,fraction=0.3"))
    ax.text(x[i]+0.02, y_max+.01, stars(regular_permuted_p_value[key]*2), horizontalalignment='center',
            verticalalignment='center')
    i += 2

ax.set_ylabel("Error")
ax.set_xticks(x)
ax.set_xticklabels(x_ticks)
ax.set_title("Mean Error of Predictive Model Across 30 Trials for each Species")
ax.legend((points[0], points[1]), ("Experiment", "Permuted Control"), loc=2,  numpoints=1, fontsize=14)
plt.xlim((x[0] - .1, x[len(x) - 1] + .1))
plt.ylim((.1, .7))
plt.show()