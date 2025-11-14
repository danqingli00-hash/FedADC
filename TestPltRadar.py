import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1, polar=True)

labelNames = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

angles = np.linspace(0, 2 * np.pi, len(labelNames), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))
feature = np.concatenate((labelNames, [labelNames[0]]))

values = [0.75, 0.05, 0.35, 0.05, 0.2, 0.5, 0.65, 0.8]
values1 = np.concatenate((values, [values[0]]))

values = [0.65, 0.8, 0.95, 0.6, 0.05, 0.2, 0.35, 0.7]
values2 = np.concatenate((values, [values[0]]))

# for i in range(len(angles)):
#     if i == len(angles) - 1:
#         ax.plot([angles[i], angles[i]], [values1[i], values2[i]], c='darkgreen', linewidth=10, linestyle="-", alpha=1)

# ax.plot(angles, values1, c='r', linewidth=3, label='Advantage Distribution p')
# ax.plot(angles, values2, c='y', linewidth=3, label='Advantage Distribution q')
# ax.fill(angles, values1, c='blue', alpha=0.75, label='Advantage Distribution p')
ax.plot(angles, values1, c='darkcyan', linewidth=5, label="thisFw", alpha=1)
# ax.fill(angles, values2, c='cyan', alpha=0.75, label='Advantage Distribution q')

ax.set_thetagrids(angles * 180 / np.pi, [], fontsize=40, style='italic')
ax.set_ylim(0, 1)
# ax.set_theta_zero_location('N')
#######################################################################
ax.set_rlabel_position(0)
plt.gca().set_yticklabels([])
# ax.set_rlabel_position(None)
# plt.legend(loc='best')
# plt.title("Client" + str(clientIdx))
#######################################################################
plt.show()