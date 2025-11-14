##################################################################################
import os
import sys

path = os.getcwd()
if path.__contains__("D:"):
    rootPath = "D:/FedAD/"
else:
    rootPath = "/autodl-tmp/FedAD/"
os.environ['HOME'] = rootPath + "FedXXX/"

sys.path.append(rootPath)
sys.path.append(os.environ['HOME'])
##################################################################################
from FedXXX.Tools import getP2List, getFormulation, \
    getAndPltMapPT2ConfList, getDynSimulation

########################################################################################
[p2LocalGoal, tNum, w1, w2, thresholdList, wayIndex2PltInfor, pNum, dNum, a1, a2, tList] = getFormulation()
########################################################################################
# pltConfSum(tNum, pNum, dNum, thresholdList, w1, w2, p2LocalGoal, wayIndex2PltInfor)
########################################################################################

########################################################################################
wayIndex = 1
_, dynMap1 = getP2List(tNum, pNum, dNum, a1, a2, w1, w2, p2LocalGoal, wayIndex)

wayIndex = 2
_, dynMap2 = getP2List(tNum, pNum, dNum, a1, a2, w1, w2, p2LocalGoal, wayIndex)
########################################################################################
mapPT2ConfList = getAndPltMapPT2ConfList(pNum, dNum, tList, dynMap1, dynMap2, wayIndex2PltInfor)
########################################################################################
mapPT2ConfList = getDynSimulation()
########################################################################################
