##################################################################################
import os
import sys


if os.getcwd().__contains__("D:"):
    rootPath = "D:/"
else:
    rootPath = "/autodl-tmp/"
os.environ['HOME'] = rootPath + "FedAD/FedXXX/"

sys.path.append(rootPath + "FedAD/")
sys.path.append(os.environ['HOME'])
##################################################################################
from FedXXX.ExpSetPy import getParaFromFile, setExp
from FedXXX.Tools import saveExpResult, prepareForOneFLExp, doExpOneDataSet
from GlobalVarSet import paraMap

##################################################################################
getParaFromFile()
##################################################################################
clientIndex2TrainTestLoaderMap, pubMap = prepareForOneFLExp()
# ##################################################################################
for ExpComIndex in list(range(len(paraMap["expCompareSetMap"]))):
    setExp(ExpComIndex)
    doExpOneDataSet(
        clientIndex2TrainTestLoaderMap,
        pubMap
    )
    saveExpResult(ExpComIndex)
# ##################################################################################
