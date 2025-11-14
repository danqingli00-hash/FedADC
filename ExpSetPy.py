import os
import ast
import datetime
import shutil
import random
import math
import torch

from GlobalVarSet import paraMap


def tran2IntList(v):
    vNew = []
    for x in v:
        vNew.append(int(x))
    return vNew


def printCoreAndDenghao(coreStr, isStart):
    if isStart:
        coreStr += " Starts"
    else:
        coreStr += " Ends"

    if len(coreStr) % 2 == 1:
        coreStr += " "

    lengthDenghao = int((180 - len(coreStr)) / 2)
    strP = "=" * lengthDenghao + coreStr + "=" * lengthDenghao
    if isStart:
        strP = "\n" + strP
    else:
        strP = strP + "\n"
    print(strP)


def generateNewID():
    timeStr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    n = str(math.floor(100000 * random.random()))
    s = "0" * (6 - len(n)) + n

    return timeStr + "_" + s


def expPSGenAndCopy():
    fileID = generateNewID()

    savePath = os.environ['HOME'] + "OutputResult/" + fileID + "/"
    os.makedirs(savePath, exist_ok=True)

    shutil.copy(
        os.environ['HOME'] + 'GenExp.txt',
        savePath + 'GenExp_' + fileID + '.txt'
    )

    print("fileID =", fileID, "\n")
    paraMap["fileID"] = fileID


def getParaFromFile():
    expPSGenAndCopy()

    kListStr, kListIntFloat, kListMap = defineParaMap()

    printParaMap(kListStr, kListIntFloat, kListMap)


def getParamInput():
    kListStr = [
        "expName",
        "dataIDUseExpSaved",
        "useNormalizeOrDirichlet"
    ]

    kListIntFloat = [
        ["clientNum", "Int"],
        ["dirichletAlpha", "Float"],

        ["usePubGen", "Int"],  # 1 means True

        ["doSoftmax", "Int"],  # 1 means True
        ["pubDataIsNonIID", "Int"],  # 1 means True
        ["pubDataTakenRatio", "Float"],
        ["trainDataTakenRatio", "Float"],
        ["pubDataMean", "Int"],
        ["pubDataVar", "Float"],

        ["centralModelIter", "Int"],
        ["outIterNum", "Int"],
        ["iterNEachOuterFirst", "Int"],
        ["iterNEachOuterAfter", "Int"],
        ["thisLr", "Float"],
        ["thisBatch", "Int"],

        ["accDisplayIterGap", "Int"],

        ["TGPTrainServerIter", "Int"]
    ]

    kListMap = ["MapDataName", "MapDataDis", "MapFramework"]

    whatDefineForExpSet = ["trainFrameWorkIndex", "PubDataDistillationTakenThreshold"]

    return kListStr, kListIntFloat, kListMap, whatDefineForExpSet


def defineParaMap():
    kListStr, kListIntFloat, kListMap, whatDefineForExpSet = getParamInput()

    expCompareSetMap = fillParam(kListStr, kListIntFloat, kListMap)

    noneSet(whatDefineForExpSet, expCompareSetMap)
    return kListStr, kListIntFloat, kListMap


def fillParam(kListStr, kListIntFloat, kListMap):
    expCompareSetMap = {}
    with open(os.environ['HOME'] + 'GenExp.txt', 'r') as file:
        content = file.read()
        for line in content.split("\n"):
            if len(line) > 0 and line[0] == "#":
                continue
            #####################################################################################
            # We will just use Dirichlet Distribution.
            # Here the problem is: how to assign different model for different clients?
            # if line.__contains__("ClientMeanVarModelType"):
            #     thisLineStr = line.split("-")[1].split(": ")[1].split(", ")
            #     paraMap["clientIndex2MeanVarModelTypeMap"][int(line.split("-")[1].split(": ")[0])] = {
            #         "Mean": int(thisLineStr[0]),
            #         "Var": float(thisLineStr[1]),
            #         "ModelType": int(thisLineStr[2])
            #     }
            #     continue
            #####################################################################################
            if line.__contains__("testExpSet"):
                expCompareSetMap[int(line.split("-")[1].split(": ")[0])] = tranExpCompare(
                    line.split("-")[1].split(": ")[1].split(", "))
                continue

            get3TypeParam(line, kListStr, kListIntFloat, kListMap)
            #####################################################################################
    return expCompareSetMap


def get3TypeParam(line, kListStr, kListIntFloat, kListMap):
    for v in kListStr:
        getStr(line, v)

    for v in kListIntFloat:
        getIntOrFloat(line, v)

    for v in kListMap:
        getMap(line, v)


def getStr(line, keyInput):
    if line.__contains__(keyInput):
        paraMap[keyInput] = line.split(keyInput + ": ")[1]


def getIntOrFloat(line, v):
    keyInput = v[0]
    isInt = v[1]
    if line.__contains__(keyInput):
        if isInt == "Int":
            paraMap[keyInput] = int(line.split(keyInput + ": ")[1])
        else:
            paraMap[keyInput] = float(line.split(keyInput + ": ")[1])


def getMap(line, v):
    if line.__contains__(v):
        paraMap[line.split("-")[0]] = ast.literal_eval(line.split("-")[1])


def expandStr(s, n):
    return s + " " * (n - len(s))


def printParaMap(kListStr, kListIntFloat, kListMap):
    printCoreAndDenghao("Basic ParaMap", True)

    for key in kListMap:
        print(expandStr(key, 16), "=", paraMap[key])

    print("\n")

    keyList = kListStr
    for v in kListIntFloat:
        keyList.append(v[0])

    for key in keyList:
        if key in ["doSoftmax", "pubDataIsNonIID", "pubDataTakenRatio",
                   "trainDataTakenRatio", "pubDataMean", "pubDataVar"]:
            continue
        print(key, "=", paraMap[key])
        if key in ["useNormalizeOrDirichlet", "dirichletAlpha", "usePubGen",
                   "pubDataVar", "iterNEachOuterAfter", "thisBatch"]:
            print("\n")

    print("\n")

    expCompareSetMap = paraMap["expCompareSetMap"]
    for i in range(len(expCompareSetMap)):
        print("expCompareSetMap", i, "=", paraMap["MapFramework"][expCompareSetMap[i][0]], expCompareSetMap[i][1])

    printCoreAndDenghao("Basic ParaMap", False)


def tranExpCompare(v):
    vNew = []
    for x in v:
        if x == "False":
            vNew.append(False)
        elif x == "True":
            vNew.append(True)
        elif x == "None":
            vNew.append(None)
        else:
            if x.__contains__("."):
                vNew.append(float(x))
            else:
                vNew.append(int(x))
    return vNew


def setExp(ExpComIndex):
    printCoreAndDenghao("ExpComIndex=" + str(ExpComIndex) + " paraMap", True)

    paraMap["ExpComIndex"] = ExpComIndex

    keyList = paraMap["whatDefineForExpSet"]
    thisExpSetting = paraMap["expCompareSetMap"][ExpComIndex]
    for i in range(len(keyList)):
        thisParam, thisValue = keyList[i], thisExpSetting[i]
        paraMap[thisParam] = thisValue
        print("thisParam and thisValue       ", thisParam, "=", thisValue)
    printCoreAndDenghao("ExpComIndex=" + str(ExpComIndex) + " paraMap", False)

    paraMap["printList"] = []


def noneSet(whatDefineForExpSet, expCompareSetMap):
    paraMap["whatDefineForExpSet"] = whatDefineForExpSet
    paraMap["expCompareSetMap"] = expCompareSetMap
    paraMap["expNum"] = len(expCompareSetMap)

    paraMap["modelTypeNum"] = 3  # This is related to genModelByExpNameAndModelType(a, b).

    paraMap["clientIndexTrainList"] = list(range(1, paraMap["clientNum"] + 1))

    paraMap["device"] = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    paraMap["criterionStu"] = torch.nn.CrossEntropyLoss().cuda()

    paraMap["teacherTypeIndex"] = 1
