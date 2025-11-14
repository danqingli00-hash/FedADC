######################################################################################################################
import os
import sys

if os.getcwd().__contains__("D:"):
    rootPath = "D:/"
else:
    rootPath = "/autodl-tmp/"

os.environ['HOME'] = rootPath + "FedAD/FedXXX/"

sys.path.append(rootPath + "FedAD/")
sys.path.append(os.environ['HOME'])
sys.path.append(os.environ['HOME'] + "ExpResAna/")
######################################################################################################################
import matplotlib.pyplot as plt

import torch
from torch.autograd import Variable
from FedXXX.Tools import getDataLC, getDataMinist

######################################################################################################################
# M
# netGenTrained = torch.load('D:/FedAD/FedXXX/OutputResult/20250716104534_037397.pth').cuda()
# concatDataset = getDataMinist()
# latentDim = 200

# L
netGenTrained = torch.load('D:/FedAD/FedXXX/OutputResult/20250715234253_085819.pth').cuda()
concatDataset = getDataLC()
latentDim = 1000
######################################################################################################################
# Use G trained to generate Img.
numImgGen = 10
print("numImgGen =", numImgGen)

netGenTrained.eval()
z = Variable(torch.randn(numImgGen, latentDim)).to("cuda:0")
genImg = netGenTrained(z)
######################################################################################################################
print("genImg.shape =", genImg.shape)
print("real data idx =", concatDataset[0][0].shape)
######################################################################################################################
for genDataIdx in [1, 2, 3]:
    plt.subplot(2, 3, genDataIdx)
    plt.imshow(genImg[genDataIdx].cpu().detach().numpy().T, cmap='viridis', interpolation='nearest', aspect='auto')

# for realDataIdx in [4, 5, 6]:
for realDataIdx in [16, 17, 18]:
    plt.subplot(2, 3, realDataIdx - 12)
    plt.imshow(concatDataset[realDataIdx][0].T, cmap='viridis', interpolation='nearest', aspect='auto')

plt.show()
######################################################################################################################
# ['20250712131126_091915', ''],  # B_0.5_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
# ['20250711215000_096563', ''],  # B_0.7_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
# ['20250712003058_080632', ''],  # B_0.9_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
#
# ['20250713234603_083070', ''],  # K_0.5_Ours, saved
# ['20250713235053_091597', ''],  # K_0.7_Ours, saved
# ['20250713235249_007780', ''],  # K_0.9_Ours, saved
############################################################################################################################
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(5)
y1 = np.array([10, 8, 7, 11, 13])
y2 = np.array([9, 6, 5, 10, 12])

bar_width = 0.3
plt.bar(x, y1, tick_label=['a', 'b', 'c', 'd', 'e'], width=bar_width)
plt.bar(x + bar_width, y2, width=bar_width)

plt.show()
############################################################################################################################
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots()

start_point = (0.1, 0.5)
end_point = (0.5, 0.1)

arrow = patches.FancyArrowPatch(start_point, end_point, arrowstyle='->', mutation_scale=20)
ax.add_patch(arrow)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.show()
############################################################################################################################
