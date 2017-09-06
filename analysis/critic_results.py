import sys 
import matplotlib.pyplot as plt

command = 'move'

regular_data = {'starfishbot':[0.151, 0.035], 'branchbot':[0.286, 0.091]}
permuted_data = {'starfishbot':[0.242, 0.088], 'branchbot':[0.384, 0.091]}
random_model = {'starfishbot':[0.817, 0.082], 'branchbot':[0.459, 0.110]}

fig, ax = plt.subplots()

x = [.15, .25, .35, .55, .65, .75]

point0 = ax.errorbar(x[2], regular_data['starfishbot'][0],
            yerr = regular_data['starfishbot'][1], 
            fmt = 'o', markersize = 5, color = 'g', ecolor = 'g')
point1 = ax.errorbar(x[1], permuted_data['starfishbot'][0],
            yerr = permuted_data['starfishbot'][1], 
            fmt = 'o', markersize = 5, color = 'r', ecolor = 'r')
point2 = ax.errorbar(x[0], random_model['starfishbot'][0],
            yerr = random_model['starfishbot'][1], 
            fmt = 'o', markersize = 5, color = 'b', ecolor = 'b')

point3 = ax.errorbar(x[5], regular_data['branchbot'][0],
            yerr = regular_data['branchbot'][1], 
            fmt = 'o', markersize = 5, color = 'g', ecolor = 'g')
point4 = ax.errorbar(x[4], permuted_data['branchbot'][0],
            yerr = permuted_data['branchbot'][1], 
            fmt = 'o', markersize = 5, color = 'r', ecolor = 'r')
point5 = ax.errorbar(x[3], random_model['branchbot'][0],
            yerr = random_model['branchbot'][1], 
            fmt = 'o', markersize = 5, color = 'b', ecolor = 'b')

ax.set_ylabel("Error")
ax.set_xticks(x)
ax.set_xticklabels(["", "Starfishbot", "", "", "Branchbot", ""])
ax.set_title("Mean Error of Predictive Model")
ax.legend((point0[0], point1[0], point2[0]), ("Experiment", "Permuted\nControl", "Random\nControl"),
        loc = 9,  numpoints = 1, fontsize = 10)
plt.xlim((x[0] - .1, x[len(x) -1] + .1))
# plt.ylim((.395, .53))

plt.show()