import ast
import os
import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt

from FedXXX.Tools import getData


def tranStr2Float100List(v):
    vNew = []
    for x in v:
        vNew.append(float(x) * 100)
    return vNew


def getFWList(fw2Plt):
    frameworkList = []
    for i in range(len(fw2Plt)):
        v = fw2Plt[len(fw2Plt) - 1 - i]
        frameworkList.append(v[0])
    return frameworkList


def getEachClient2AccListMapList(fileID, rMap):
    idx2Client2AccListMapMap = {}
    idx2Client2Maf1ListMapMap = {}
    idx2Client2Mif1ListMapMap = {}
    idx2Client2RaListMapMap = {}
    for idx in range(rMap["expNum"]):
        thisValue = getEachClient2AccListMap(fileID, idx, rMap, "acc")
        if thisValue is not None:
            idx2Client2AccListMapMap[idx] = thisValue

        thisValue = getEachClient2AccListMap(fileID, idx, rMap, "maf1")
        if thisValue is not None:
            idx2Client2Maf1ListMapMap[idx] = thisValue

        thisValue = getEachClient2AccListMap(fileID, idx, rMap, "mif1")
        if thisValue is not None:
            idx2Client2Mif1ListMapMap[idx] = thisValue

        thisValue = getEachClient2AccListMap(fileID, idx, rMap, "radar")
        if thisValue is not None:
            idx2Client2RaListMapMap[idx] = thisValue
    return idx2Client2AccListMapMap, idx2Client2Maf1ListMapMap, idx2Client2Mif1ListMapMap, idx2Client2RaListMapMap


def getValueFromList(fw2Plt, fw, index):
    for v in fw2Plt:
        if fw == v[0]:
            return v[index + 1]


def pltAcc(fileIDList, fileID, expNum, clientNum, MapFramework, fw2Plt, eachClient2AccListMapList, centralAcc,
           thisTitle, isLegend):
    for clientIndex in range(1, clientNum + 1):
        plt.subplot(len(fileIDList), clientNum, fileIDList.index(fileID) * clientNum + clientIndex)
        iterLength = None
        for expIndex in range(expNum):
            if eachClient2AccListMapList[expIndex] is None:
                continue
            thisColor = getValueFromList(fw2Plt, MapFramework[expIndex], 0)
            thisLineWidth = getValueFromList(fw2Plt, MapFramework[expIndex], 1)
            thisLineStyle = getValueFromList(fw2Plt, MapFramework[expIndex], 2)
            thisAlpha = getValueFromList(fw2Plt, MapFramework[expIndex], 3)
            iterLength = len(eachClient2AccListMapList[expIndex][clientIndex])
            plt.plot(
                eachClient2AccListMapList[expIndex][clientIndex],
                color=thisColor,
                linestyle=thisLineStyle,
                alpha=thisAlpha,
                linewidth=thisLineWidth,
                label=MapFramework[expIndex]
            )
        plt.plot(
            [centralAcc] * iterLength,
            color="k", linestyle="--", alpha=0.5, linewidth=3, label="CentralTrain"
        )
        plt.ylim(0, 100)
        plt.xlabel('Iteration', fontsize=14, color='k')
        plt.ylabel('Acc', fontsize=14, color='k')
        plt.title(thisTitle + " Client" + str(clientIndex))

        if isLegend:
            plt.legend()

        plt.grid()


def getEachFramework2AccMap(idx2Client2AccListMapMap, p):
    idx2AverageAccListMap = {}
    idx2AccMap = {}
    for idx in idx2Client2AccListMapMap.keys():
        thisAverageAccList = getAllClientsAverageAccMap(idx2Client2AccListMapMap[idx])
        idx2AverageAccListMap[idx] = thisAverageAccList

        lastN = int(p * len(thisAverageAccList))
        idx2AccMap[idx] = round(sum(thisAverageAccList[-lastN:]) / lastN, 3)
    return idx2AverageAccListMap, idx2AccMap


def getPaperResult(fileIDListInput, averageLastRatio):
    fileIDList = getFileIDList(fileIDListInput)

    (fileID2RMap, fileID2DsMap,
     fileID2Idx2Client2AccListMapMap, fileID2Idx2AverageAccMap, fileID2Idx2AccMap,
     fileID2Idx2Client2Maf1ListMapMap, fileID2Idx2AverageMaf1Map, fileID2Idx2Maf1Map,
     fileID2Idx2Client2Mif1ListMapMap, fileID2Idx2AverageMif1Map, fileID2Idx2Mif1Map,
     fileIDIdxClient2RadarMap, fileID2Iter2RShipMap, fileID2LabelNamesMap, fileID2TrainTestDataNumSizeMap) = (
        getResultEachFileID(fileIDList, averageLastRatio))

    tableMapAccMaf1Mif1 = (
        resultsTable(
            fileIDList,
            fileID2Idx2Client2AccListMapMap, fileID2RMap,
            fileID2Idx2AccMap, fileID2Idx2Maf1Map, fileID2Idx2Mif1Map
        ))
    title2IdxMap = getTitle2IdxMap(fileIDList, fileID2RMap)
    return (fileIDList, fileID2RMap, fileID2DsMap,
            fileID2Idx2Client2AccListMapMap, fileID2Idx2AverageAccMap, fileID2Idx2AccMap,
            fileID2Idx2Client2Maf1ListMapMap, fileID2Idx2AverageMaf1Map, fileID2Idx2Maf1Map,
            fileID2Idx2Client2Mif1ListMapMap, fileID2Idx2AverageMif1Map, fileID2Idx2Mif1Map,
            fileIDIdxClient2RadarMap, fileID2Iter2RShipMap, fileID2LabelNamesMap, fileID2TrainTestDataNumSizeMap,
            tableMapAccMaf1Mif1, title2IdxMap)


def getRobustTestOutput(pltIndex, outputFile, robustTestFileIDList, fileID2RMap, fileID2Idx2AccMap,
                        thresholdValueList):
    robustIdxList = list(range(len(thresholdValueList)))
    if pltIndex != 1:
        print("Wrong! pltIndex != 1")
        return

    pList = ["\\" + "begin{center}", "\\" + "begin{adjustbox}{width=1.0" + "\\" + "textwidth}",
             "\\" + "begin{tabular}{" + "p{15mm}" * (
                     1 + len(robustTestFileIDList) * len(robustTestFileIDList[0])) + "}", "\\" + "toprule",
             "\\" + "cmidrule(r){1-" + str(1 + len(robustTestFileIDList) * len(robustTestFileIDList[0])) + "}"]

    s = "\\" + "multirow{2}{1cm}{" + "\\" + "centering " + "\\" + "textbf{Conf Value}} "
    for fileID in robustTestFileIDList[0]:
        s += "& " + "\\" + "multicolumn{2}{c}{" + "\\" + "textbf{" + fileID2RMap[fileID]['thisTitle'].split("-")[
            0] + "}} "
    s += "\\" + "\\"
    pList.append(s)

    a = ""
    for i in range(len(robustTestFileIDList[0])):
        a += "\\" + "cmidrule(r){" + str(2 + len(robustTestFileIDList) * i) + "-" + str(
            1 + len(robustTestFileIDList) * (i + 1)) + "}"
    pList.append(a)

    a = ""
    for i in range(len(robustTestFileIDList)):
        a += "& D" + str(i + 1) + " "
    a = a * len(robustTestFileIDList[0])

    pList.append(a + "\\" + "\\")

    pList.append("\\" + "cmidrule(r){1-" + str(1 + len(robustTestFileIDList) * len(robustTestFileIDList[0])) + "}")

    for k in robustIdxList:
        # if thresholdValueList[k] in ["0.75", "0.80"]:
        if False:
            a = "\\" + "textbf{" + thresholdValueList[k] + "} "
        else:
            a = thresholdValueList[k] + " "
        for i in range(len(robustTestFileIDList[0])):
            if k in fileID2Idx2AccMap[robustTestFileIDList[0][i]].keys():
                value1 = fileID2Idx2AccMap[robustTestFileIDList[0][i]][k]
            else:
                value1 = "X"
            if k in fileID2Idx2AccMap[robustTestFileIDList[1][i]].keys():
                value2 = fileID2Idx2AccMap[robustTestFileIDList[1][i]][k]
            else:
                value2 = "X"
            # if thresholdValueList[k] in ["0.75", "0.80"]:
            if False:
                a += ("& " + "\\" + "textbf{" + str(value1) +
                      "} & " + "\\" + "textbf{" + str(value2) + "} ")
            else:
                a += ("& " + str(value1) +
                      " & " + str(value2) + " ")
        a += "\\" + "\\"
        pList.append(a)

    pList.append("\\" + "cmidrule(r){1-" + str(1 + len(robustTestFileIDList) * len(robustTestFileIDList[0])) + "}")
    pList.append("\\" + "end{tabular}")
    pList.append("\\" + "end{adjustbox}")
    pList.append("\\" + "end{center}")

    with open(outputFile, 'w') as file:
        for s in pList:
            file.write(s + '\n')


def getFileIDIdxClient2RadarMap(fileIDList, fileID2RMap, fileID2DsMap, fileID2Idx2Client2RaListMapMap):
    fileIDIdxClient2RadarMap = {}
    for fileID in fileIDList:
        idxListList = getIdxListList(fileID2RMap, fileID2DsMap, fileID)
        for idx in fileID2Idx2Client2RaListMapMap[fileID].keys():
            thisClient2Ra = fileID2Idx2Client2RaListMapMap[fileID][idx]
            if thisClient2Ra is not None:
                for clientIdx in thisClient2Ra.keys():
                    fileIDIdxClient2RadarMap[fileID + "-" + str(idx) + "-" + str(clientIdx)] = (
                        cutList(thisClient2Ra[clientIdx], idxListList))
    return fileIDIdxClient2RadarMap


def pltRadarTwoClients():
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1, polar=True)

    labelNames = ['a', 'b', 'c', 'd', 'e']

    angles = np.linspace(0, 2 * np.pi, len(labelNames), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    feature = np.concatenate((labelNames, [labelNames[0]]))

    values = [0.1, 0.2, 0.3, 0.4, 0.5]
    values = np.concatenate((values, [values[0]]))
    # ax.plot(angles, values, c=cMap[fwMap[k]], linewidth=0.5, label=fwMap[k])
    ax.fill(angles, values, c='r', alpha=0.7, label="thisFw")

    # ax.set_thetagrids(angles * 180 / np.pi, feature, fontsize=10, style='italic')
    #######################################################################
    ax.set_ylim(0, 100)
    # ax.set_theta_zero_location('N')
    #######################################################################
    # ax.set_rlabel_position(0)
    # plt.legend(legendList, loc='best')
    # plt.title("Client" + str(clientIdx))
    #######################################################################
    plt.show()


def getTitle2IdxMap(fileIDList, fileID2RMap):
    title2IdxMap = {}
    for idx in range(len(fileIDList)):
        title2IdxMap[fileID2RMap[fileIDList[idx]]['thisTitle']] = idx
    print(title2IdxMap)
    return title2IdxMap


def pltDynResults(dynMap, clientIdx, thisSimuIterIdx, labelNum, ax, angles, ifShadow, dynIdx):
    if dynIdx == 1:
        colorInput = "k"
        labelName = "FedMD"
        alphaV = 0.8
    else:
        colorInput = "blue"
        labelName = "Ours"
        alphaV = 0.6

    confList = []
    for dIndex in range(1, labelNum + 1):
        confList.append(100 * dynMap[clientIdx][dIndex][thisSimuIterIdx])

    values = np.concatenate((confList, [confList[0]]))
    if ifShadow:
        ax.fill(angles, values, c=colorInput, linewidth=0.001, alpha=alphaV, label=labelName)
    else:
        ax.plot(angles, values, c=colorInput, linewidth=1.5, label=labelName, linestyle="--")

    return values


def divide100V(v):
    vNew = []
    for x in v:
        vNew.append(float(x) / 100)
    return vNew


def getVSumList(v):
    vSumList = []
    for x in v:
        vSumList.append(sum(x))
    return vSumList


def pltTrail(v, ax, patches, fwInput, clientInput, isReal):
    xList = []
    yList = []
    for x in v:
        xList.append(x[0])
        yList.append(x[1])

    if fwInput == "Ours70":
        colorInput = 'blue'
        lineW = 2
        pS = 50
    if fwInput == "FedMD":
        colorInput = 'black'
        lineW = 2
        pS = 40

    if isReal:
        linestyleHere = "-"
    else:
        linestyleHere = "--"

    for i in range(1, len(v)):
        start_point = (v[i - 1][0], v[i - 1][1])
        end_point = (v[i][0], v[i][1])
        arrow = patches.FancyArrowPatch(start_point, end_point, color=colorInput, linewidth=lineW,
                                        linestyle=linestyleHere,
                                        arrowstyle='->', mutation_scale=20)
        ax.add_patch(arrow)

    plt.scatter(xList, yList, s=pS, color=colorInput, alpha=1, label=fwInput)


def getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesMap):
    v = []
    for i in list(range(0, 15, 2)):
        thisKey = str(i) + "-" + str(clientInput) + "-" + fwInput
        v.append([iterIdx2ClientFwValuesMap[thisKey][d1], iterIdx2ClientFwValuesMap[thisKey][d2]])
    return v


def pltRadar(
        pltIndex,
        fileID,
        nPlt, cMap, alphaMap,
        iterNum, labelNames, clientNum,
        fwMap, fileIDIdxClient2RadarMap, ifShadow, dynMap1, dynMap2, tNum
):
    if pltIndex != 0:
        print("wrong! pltIndex != 0")
        return None

    iterPltList = getIterPltList(iterNum, nPlt)
    fig = plt.figure(figsize=(8, 8))

    angles = np.linspace(0, 2 * np.pi, len(labelNames), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))
    feature = np.concatenate((labelNames, [labelNames[0]]))

    iterIdx2ClientFwValuesMap = {}
    iterIdx2ClientFwValuesDynMap = {}

    valuesDynFedMD = None
    valuesDynOurs = None
    for iterIdx in iterPltList:
        ############################################################################################
        thisSimuIterIdx = int(float(iterIdx) / iterNum * tNum) + 1
        # thisSimuIterIdx = tNum - 1
        ############################################################################################
        # print("thisSimuIterIdx =", thisSimuIterIdx)
        for clientIdx in range(1, clientNum + 1):
            ax = fig.add_subplot(len(iterPltList), clientNum, clientIdx + iterPltList.index(iterIdx) * clientNum,
                                 polar=True)
            ###########################################################################################
            labelNum = len(labelNames)
            ###########################################################################################
            valuesDynOurs = pltDynResults(dynMap2, clientIdx, thisSimuIterIdx, labelNum, ax, angles, ifShadow, 2)
            valuesDynFedMD = pltDynResults(dynMap1, clientIdx, thisSimuIterIdx, labelNum, ax, angles, ifShadow, 1)
            if valuesDynFedMD is not None:
                iterIdx2ClientFwValuesDynMap[str(iterIdx) + "-" + str(clientIdx) + "-FedMD"] = valuesDynFedMD.tolist()
            if valuesDynOurs is not None:
                iterIdx2ClientFwValuesDynMap[str(iterIdx) + "-" + str(clientIdx) + "-Ours70"] = valuesDynOurs.tolist()
            ###########################################################################################
            legendList = []
            for idx in fwMap.keys():
                thisFw = fwMap[idx]
                thisKey = fileID + "-" + str(idx) + "-" + str(clientIdx)
                if thisKey in fileIDIdxClient2RadarMap.keys():
                    values = fileIDIdxClient2RadarMap[thisKey][iterIdx]
                    values = np.concatenate((values, [values[0]]))
                    ###########################################################################################
                    iterIdx2ClientFwValuesMap[str(iterIdx) + "-" + str(clientIdx) + "-" + str(thisFw)] = values.tolist()
                    ###########################################################################################
                    # if ifShadow:
                    #     ax.fill(angles, values, c=cMap[thisFw], linewidth=0.001, alpha=alphaMap[thisFw], label=thisFw)
                    # else:
                    #     ax.plot(angles, values, c=cMap[thisFw], linewidth=1.5, label=thisFw, alpha=0.7)
                    ###########################################################################################
                    legendList.append(thisFw)
            #######################################################################
            # ax.set_thetagrids(angles * 180 / np.pi, feature, fontsize=10, style='italic')
            #######################################################################
            ax.set_ylim(0, 100)
            # ax.set_thetagrids(angles * 180 / np.pi, feature, fontsize=5, style='italic')
            ax.set_thetagrids(angles * 180 / np.pi, [], fontsize=5, style='italic')
            # ax.set_theta_zero_location('N')
            plt.gca().set_yticklabels([])
            #######################################################################
            ax.set_rlabel_position(0)
            # plt.legend(legendList, loc='best')
            # plt.title("Client" + str(clientIdx))
            #######################################################################
    plt.show()

    return iterIdx2ClientFwValuesMap, iterIdx2ClientFwValuesDynMap


def pltThresholdTestNew(tableMapAccMaf1Mif1, dataNameList, qList, pList):
    x = np.arange(6)
    bar_width = 0.9

    count = 0
    for dataName in dataNameList:
        for q in qList:
            #########################################################
            if dataName not in ['btumor', 'knee'] and q > 0.3:
                continue
            #########################################################
            count += 1
            plt.subplot(len(dataNameList), len(qList), count)
            # plt.subplot(4, 4, count)

            s = []
            for p in pList:
                thisKey = dataName + "-Ours-" + str(p) + "-" + str(q)
                if thisKey in tableMapAccMaf1Mif1.keys():
                    s.append(float(tableMapAccMaf1Mif1[thisKey][0]))
            if s and len(s) == 6:
                plt.bar(x, np.array(s), color='lightblue', tick_label=['a', 'b', 'c', 'd', 'e', 'f'], width=bar_width)
                maxIdx = s.index(max(s))
                # print(s, maxIdx)
                # print(x[maxIdx], np.array(s)[maxIdx])
                plt.bar(x[maxIdx], np.array(s)[maxIdx], color='darkblue', width=bar_width)
                plt.plot(x, np.array(s), color='black', marker='o', linestyle='-', linewidth=0.6,
                         label='Line Values')

            plt.title({'btumor': 'Btumor'}[dataName] + "-" + str(q), fontsize=14)
            plt.xticks(list(range(len(pList))), pList, fontsize=14, rotation=60)
            if count in [1, 6]:
                plt.ylabel("Acc", fontsize=14)
            plt.xlabel("Confidence Threshold", fontsize=14)
            # plt.legend()
    plt.show()


def pltBetaCompare(fw2Plt, fwList, betaList, dataNameHere, tableMapAccMaf1Mif1, perIdx, dataNamePltIdxMap):
    for fwName in fwList:
        if fwName == 'Ours':
            thisFwName = 'Ours-0.90'
        else:
            thisFwName = fwName

        vList = []
        for beta in betaList:
            thisKey = dataNameHere + '-' + thisFwName + '-' + beta
            if thisKey in tableMapAccMaf1Mif1.keys():
                vList.append(float(tableMapAccMaf1Mif1[thisKey][perIdx]))
            else:
                vList.append(0)

        thisColor = getValueFromList(fw2Plt, thisFwName, 0)
        thisLineWidth = getValueFromList(fw2Plt, thisFwName, 1)
        thisLineStyle = getValueFromList(fw2Plt, thisFwName, 2)
        thisAlpha = getValueFromList(fw2Plt, thisFwName, 3)

        plt.subplot(1, 1, dataNamePltIdxMap[dataNameHere])

        # print("thisFwName =", thisFwName)
        if thisFwName.__contains__("Ours"):
            lw = 5
            thisColor = 'darkblue'
            thisAlpha = 0.95
            thisFwName = "FedADC"
        else:
            lw = 2

        plt.plot(
            vList,
            color=thisColor,
            linestyle=thisLineStyle, marker='^',
            alpha=thisAlpha,
            linewidth=lw,
            label=thisFwName
        )
    plt.xlabel("Beta", fontsize=18)
    plt.ylabel("Acc", fontsize=18)
    plt.xticks(list(range(len(betaList))), betaList, fontsize=18)
    plt.yticks(fontsize=18)
    plt.title({"btumor": 'Btumor'}[dataNameHere], fontsize=18)
    plt.legend()
    plt.show()


def pltThresholdTest(tableMapAccMaf1Mif1, dataNameList, qList, pList):
    # import numpy as np
    # import matplotlib.pyplot as plt
    x = np.arange(6)
    # y1 = np.array([10, 8, 7, 11, 13])
    # y2 = np.array([9, 6, 5, 10, 12])

    bar_width = 0.1
    # plt.bar(x, y1, tick_label=['a', 'b', 'c', 'd', 'e'], width=bar_width)
    # plt.bar(x + bar_width, y2, width=bar_width)
    # plt.show()

    c = 0
    count = 0
    for dataName in dataNameList:
        for q in qList:
            s = []
            c += 1
            for p in pList:
                thisKey = dataName + "-Ours-" + str(p) + "-" + str(q)
                if thisKey in tableMapAccMaf1Mif1.keys():
                    s.append(float(tableMapAccMaf1Mif1[thisKey][0]))
            if s and len(s) == 6:
                # plt.plot(s, linewidth=3, label=dataName + "-" + str(q))
                plt.bar(x + bar_width * count, np.array(s), tick_label=['a', 'b', 'c', 'd', 'e', 'f'], width=bar_width)
                count += 1
    plt.xticks(list(range(len(pList))), pList)
    plt.ylabel("Acc")
    plt.xlabel("Conf Threshold")
    # plt.legend()


def getIterPltList(iterNum, nPlt):
    N = iterNum - 2
    step = math.ceil(float(N) / (nPlt - 1))

    iterPltList = [0]
    for i in range(1, nPlt):
        thisGap = i * step
        if thisGap <= N:
            iterPltList.append(thisGap)
    if iterNum - 2 not in iterPltList:
        iterPltList.append(iterNum - 2)
    print(iterPltList)
    return iterPltList


def estimateEndTime(a1, a2, outN, clientN):
    s1 = [int(a1.split(":")[0]), int(a1.split(":")[1])]
    s2 = [int(a2.split(":")[0]), int(a2.split(":")[1])]
    s3 = [s2[0] - 1, s2[1] + 60]
    q = s3[1] - s1[1] + 60 * (s3[0] - s1[0])

    hResult = round(q * 8 * (7 - clientN + (16 - outN) * 6) / 3600, 2)
    dResult = round(hResult / 24, 2)
    print(str(hResult) + "H", str(dResult) + "D")


def getExpFileIDJustBenchmarks(benchmarkPlt):
    fw2Plt = benchmarkPlt

    fileIDListInput = [
        ['20250616190753_050361', ''],  # M_0.1 (15 fw) # FedGEMS is wrong
        ['20250618141254_025423', ''],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
        ['20250620220350_018565', ''],  # L_0.1_50data, (0Ours, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        ['20250618142044_000804', ''],  # B_0.1 (15 fw) + run Cronus
        ['20250618143322_034012', ''],  # K_0.1 (15 fw), + run Cronus

        ['20250619111335_018997', ''],  # M_0.3 (15 fw)
        ['20250619111551_013657', ''],  # S_0.3 (15 fw) + run Cronus
        ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        ['20250619160516_027627', ''],  # B_0.3 (15 fw) + run Cronus
        ['20250619111744_055767', ''],  # K_0.3 (15 fw), + run Cronus

        ['20250712131126_091915', ''],  # B_0.5_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
        ['20250711215000_096563', ''],  # B_0.7_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
        ['20250712003058_080632', ''],  # B_0.9_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved

        ['20250713234603_083070', ''],  # K_0.5_Ours, saved
        ['20250713235053_091597', ''],  # K_0.7_Ours, saved
        ['20250713235249_007780', ''],  # K_0.9_Ours, saved

        ['20250624095904_078609', '-'],  # M_0.1_65-70-75-80-85-90 (added)
        ['20250621151912_083574', '-'],  # M_0.3_65-70-75-80-85-90 (added)

        ['20250624140511_099715', '-'],  # S_0.1_65-70-75-80-85-90 (added)
        ['20250624233644_021352', '-'],  # S_0.3_65-70-75-80-85-90 (added)

        ['20250625231904_057633', '-'],  # L_0.1_65-70-75
        ['20250625224910_012705', '-'],  # L_0.3_65-70 (running)

        ['20250623211522_087167', '-'],  # B_0.1_65-70-75-80-85-90 (added)
        ['20250621081442_055955', '-'],  # B_0.3_65-70-75-80-85-90 (added)

        ['20250623212407_065360', '-'],  # K_0.1_65-70-75-80-85-90 (added)
        ['20250621075843_084608', '-'],  # K_0.3_65-70-75-80-85-90 (added)
    ]

    return fw2Plt, fileIDListInput


def getExpFileIDJustOursAndFedMD():
    fw2Plt = [
        ["Ours-0.65", "red", 3, "-", 0.8],
        ["Ours-0.70", "yellow", 3, "-", 0.8],
        ["Ours-0.75", "blue", 3, "-", 0.8],
        ["Ours-0.80", "green", 3, "-", 0.8],
        ["Ours-0.85", "cyan", 3, "-", 0.8],
        ["Ours-0.90", "purple", 3, "-", 0.8],

        # ["FedAPEN", "red", 1, "-", 1.0],
        # ["FedTGP", "yellow", 1, "-", 1.0],
        # ["Cronus", "blue", 1, "-", 1.0],
        # ["FedDF", "green", 1, "-", 1.0],
        # ["FedProto", "violet", 1, "-", 1.0],
        # ["FedGEMS", "black", 1, "-", 1.0],
        ["FedMD", "black", 3, "--", 1.0],
        # ["FedProx", "purple", 1, "-", 1.0],
        # ["FedAvg", "tomato", 1, "-", 1.0],
    ]

    fileIDListInput = [
        ['20250616190753_050361', ''],  # M_0.1 (15 fw) # FedGEMS is wrong
        ['20250624095904_078609', '-'],  # M_0.1_65-70-75-80-85-90 (added)

        ['20250619111335_018997', ''],  # M_0.3 (15 fw)
        ['20250621151912_083574', '-'],  # M_0.3_65-70-75-80-85-90 (added)

        ['20250618141254_025423', ''],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
        ['20250624140511_099715', '-'],  # S_0.1_65-70-75-80-85-90 (added)

        ['20250619111551_013657', ''],  # S_0.3 (15 fw) + run Cronus
        ['20250624233644_021352', '-'],  # S_0.3_65-70-75-80-85-90 (added)
        # ['20250630161204_093662'], rerun S_0.3_Prox-Avg thisLr: 0.0001 thisBatch: 128 added
        # ['20250630194747_053931'], rerun S_0.3_FedDF thisLr: 0.0001 thisBatch: 16 added

        ['20250618142044_000804', ''],  # B_0.1 (15 fw) + run Cronus
        ['20250623211522_087167', '-'],  # B_0.1_65-70-75-80-85-90 (added)
        # ['20250630170147_074618'], rerun B_0.1_APEN, running
        # ['20250701100758_075500'], rerun B_0.1_Proto, running

        ['20250619160516_027627', ''],  # B_0.3 (15 fw) + run Cronus
        ['20250621081442_055955', '-'],  # B_0.3_65-70-75-80-85-90 (added)
        # ['20250630170406_056207'], rerun B_0.3_APEN, running

        ['20250618143322_034012', ''],  # K_0.1 (15 fw), + run Cronus
        ['20250623212407_065360', '-'],  # K_0.1_65-70-75-80-85-90 (added)
        # ['20250630231158_039371'], rerun K_0.1_FedDF thisLr: 0.0001 thisBatch: 16 added

        ['20250619111744_055767', ''],  # K_0.3 (15 fw), + run Cronus
        ['20250621075843_084608', '-'],  # K_0.3_65-70-75-80-85-90 (added)

        ['20250620220350_018565', ''],
        # L_0.1_50data, (0Ours, 1FedAPEN, 2FedTGP, 3FedDF, 6FedProto, 7FedMD, 8FedProx, 9FedAvg)
        # 65: 0(added),    70: 10,    75: 11,    80: 12(added),    85: 13(added),    90: 14(added)
        # (20250620220350_018565, 0Ours added 1FedAPEN added 2TGP added) + (3FedDF added) + (20250626094240_078275, 6Proto added) + (20250628124029_089298, MD added) + (20250626110930_073187, Prox-Avg added)
        ['20250625231904_057633', '-'],  # L_0.1_65(added)-70-75  (running)
        # 65: 0(added),    70: 1,    75: 2,    80: 3(added),    85: 4(added),    90: 5(added)
        # '20250626150128_071769',  # L_0.1_85(added)-90(added)

        ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 1FedAPEN, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        # 65: 0(added),    70: 10(added),    75: 11,    80: 12(added),    85: 13(added),    90: 14
        # (20250622000033_074801, Ours-APEN added) + (20250629212840_044334, TGP running) + (3FedDF added) + (20250626094433_009690, 6Proto added, MD running) + (20250626112546_013381, Prox-Avg added)
        ['20250625224910_012705', '-'],  # L_0.3_65-70
        # 65: 0(added),    70: 1(added),    75: 2,    80: 3(added),    85: 4(added),    90: 5
        # ['20250629153336_069793', ''],  # L_0.3_75 (running)
        # '20250626150738_093495',  # L_0.3_85(added)
        # '20250630150107_008277',  # L_0.3_90 (running)
    ]

    return fw2Plt, fileIDListInput


def getExpFileIDJustOursAndFedMDForLC03():
    fw2Plt = [
        ["Ours-0.65", "red", 3, "-", 0.8],
        ["Ours-0.70", "yellow", 3, "-", 0.8],
        ["Ours-0.75", "blue", 3, "-", 0.8],
        ["Ours-0.80", "green", 3, "-", 0.8],
        ["Ours-0.85", "cyan", 3, "-", 0.8],
        ["Ours-0.90", "purple", 3, "-", 0.8],

        # ["FedAPEN", "red", 1, "-", 1.0],
        # ["FedTGP", "yellow", 1, "-", 1.0],
        # ["Cronus", "blue", 1, "-", 1.0],
        # ["FedDF", "green", 1, "-", 1.0],
        # ["FedProto", "violet", 1, "-", 1.0],
        # ["FedGEMS", "black", 1, "-", 1.0],
        ["FedMD", "black", 3, "--", 1.0],
        # ["FedProx", "purple", 1, "-", 1.0],
        # ["FedAvg", "tomato", 1, "-", 1.0],
    ]

    fileIDListInput = [
        ['20250616190753_050361', '-'],  # M_0.1 (15 fw) # FedGEMS is wrong
        ['20250624095904_078609', '-'],  # M_0.1_65-70-75-80-85-90 (added)

        ['20250619111335_018997', '-'],  # M_0.3 (15 fw)
        ['20250621151912_083574', '-'],  # M_0.3_65-70-75-80-85-90 (added)

        ['20250618141254_025423', '-'],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
        ['20250624140511_099715', '-'],  # S_0.1_65-70-75-80-85-90 (added)

        ['20250619111551_013657', '-'],  # S_0.3 (15 fw) + run Cronus
        ['20250624233644_021352', '-'],  # S_0.3_65-70-75-80-85-90 (added)
        # ['20250630161204_093662'], rerun S_0.3_Prox-Avg thisLr: 0.0001 thisBatch: 128 added
        # ['20250630194747_053931'], rerun S_0.3_FedDF thisLr: 0.0001 thisBatch: 16 added

        ['20250618142044_000804', '-'],  # B_0.1 (15 fw) + run Cronus
        ['20250623211522_087167', '-'],  # B_0.1_65-70-75-80-85-90 (added)
        # ['20250630170147_074618'], rerun B_0.1_APEN, running
        # ['20250701100758_075500'], rerun B_0.1_Proto, running

        ['20250619160516_027627', '-'],  # B_0.3 (15 fw) + run Cronus
        ['20250621081442_055955', '-'],  # B_0.3_65-70-75-80-85-90 (added)
        # ['20250630170406_056207'], rerun B_0.3_APEN, running

        ['20250618143322_034012', '-'],  # K_0.1 (15 fw), + run Cronus
        ['20250623212407_065360', '-'],  # K_0.1_65-70-75-80-85-90 (added)
        # ['20250630231158_039371'], rerun K_0.1_FedDF thisLr: 0.0001 thisBatch: 16 added

        ['20250619111744_055767', '-'],  # K_0.3 (15 fw), + run Cronus
        ['20250621075843_084608', '-'],  # K_0.3_65-70-75-80-85-90 (added)

        ['20250620220350_018565', '-'],
        # L_0.1_50data, (0Ours, 1FedAPEN, 2FedTGP, 3FedDF, 6FedProto, 7FedMD, 8FedProx, 9FedAvg)
        # 65: 0(added),    70: 10,    75: 11,    80: 12(added),    85: 13(added),    90: 14(added)
        # (20250620220350_018565, 0Ours added 1FedAPEN added 2TGP added) + (3FedDF added) + (20250626094240_078275, 6Proto added) + (20250628124029_089298, MD added) + (20250626110930_073187, Prox-Avg added)
        ['20250625231904_057633', '-'],  # L_0.1_65(added)-70-75  (running)
        # 65: 0(added),    70: 1,    75: 2,    80: 3(added),    85: 4(added),    90: 5(added)
        # '20250626150128_071769',  # L_0.1_85(added)-90(added)

        ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 1FedAPEN, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        # 65: 0(added),    70: 10(added),    75: 11,    80: 12(added),    85: 13(added),    90: 14
        # (20250622000033_074801, Ours-APEN added) + (20250629212840_044334, TGP running) + (3FedDF added) + (20250626094433_009690, 6Proto added, MD running) + (20250626112546_013381, Prox-Avg added)
        ['20250625224910_012705', '-'],  # L_0.3_65-70
        # 65: 0(added),    70: 1(added),    75: 2,    80: 3(added),    85: 4(added),    90: 5
        # ['20250629153336_069793', ''],  # L_0.3_75 (running)
        # '20250626150738_093495',  # L_0.3_85(added)
        # '20250630150107_008277',  # L_0.3_90 (running)
    ]

    return fw2Plt, fileIDListInput


def basicInfor():
    averageLastRatio = 0.3

    dataName2SourceMap = {
        "M": "http://yann.lecun.com/exdb/mnist/",
        "S": "https://www.kaggle.com/datasets/mahmoudreda55/satellite-image-classification",
        "L": "Borkowski A A, Bui M M, Thomas L B, et al. Lung and colon cancer histopathological image dataset (lc25000)[J]. arXiv preprint arXiv:1912.12142, 2019.",
        "B": "https://github.com/sartajbhuvaji/brain-tumor-classification-dataset",
        "K": "Chen, Pingjun (2018), 'Knee Osteoarthritis Severity Grading Dataset', Mendeley Data, V1, doi: 10.17632/56rmx5bjcr.1",
    }

    outputFile1 = os.environ['HOME'] + "ExpResAna/DataStatistics_Result.txt"
    outputFile2 = os.environ['HOME'] + "ExpResAna/Experiment_Result.txt"
    outputFile3 = os.environ['HOME'] + "ExpResAna/RobustTest_Result.txt"

    return averageLastRatio, dataName2SourceMap, outputFile1, outputFile2, outputFile3


def getExpFileIDJustOurs(oursPlt):
    fw2Plt = oursPlt

    fileIDListInput = [
        ['20250616190753_050361', '-'],  # M_0.1 (15 fw) # FedGEMS is wrong
        ['20250618141254_025423', '-'],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
        ['20250620220350_018565', '-'],  # L_0.1_50data, (0Ours, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        ['20250618142044_000804', '-'],  # B_0.1 (15 fw) + run Cronus
        ['20250618143322_034012', '-'],  # K_0.1 (15 fw), + run Cronus

        ['20250619111335_018997', '-'],  # M_0.3 (15 fw)
        ['20250619111551_013657', '-'],  # S_0.3 (15 fw) + run Cronus
        ['20250622000033_074801', '-'],  # L_0.3_50data, (0Ours, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        ['20250619160516_027627', '-'],  # B_0.3 (15 fw) + run Cronus
        ['20250619111744_055767', '-'],  # K_0.3 (15 fw), + run Cronus

        ['20250624095904_078609', ''],  # M_0.1_65-70-75-80-85-90 (added)
        ['20250624140511_099715', ''],  # S_0.1_65-70-75-80-85-90 (added)
        ['20250625231904_057633', ''],  # L_0.1_65-70-75
        ['20250623211522_087167', ''],  # B_0.1_65-70-75-80-85-90 (added)
        ['20250623212407_065360', ''],  # K_0.1_65-70-75-80-85-90 (added)

        ['20250621151912_083574', ''],  # M_0.3_65-70-75-80-85-90 (added)
        ['20250624233644_021352', ''],  # S_0.3_65-70-75-80-85-90 (added)
        ['20250625224910_012705', ''],  # L_0.3_65-70 (running)
        ['20250621081442_055955', ''],  # B_0.3_65-70-75-80-85-90 (added)
        ['20250621075843_084608', ''],  # K_0.3_65-70-75-80-85-90 (added)

        ['20250712131126_091915', ''],  # B_0.5_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
        ['20250711215000_096563', ''],  # B_0.7_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
        ['20250712003058_080632', ''],  # B_0.9_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved

        ['20250713234603_083070', ''],  # K_0.5_Ours, saved
        ['20250713235053_091597', ''],  # K_0.7_Ours, saved
        ['20250713235249_007780', ''],  # K_0.9_Ours, saved
    ]

    return fw2Plt, fileIDListInput


def pltAccFcn(idxAndIfPlt, fileIDList, fileID2RMap, fileID2DsMap, fileID2Idx2AverageAccMap, fw2Plt, isLegend,
              isPltFill):
    idxList = []
    pltIdxMap = {}
    for v in idxAndIfPlt:
        idxList.append(v[0])
        pltIdxMap[v[0]] = v[1]

    valueSum = sum(pltIdxMap.values())
    [nRow, nCol] = getRowAndCol(len(fileIDList))
    nRow = nRow * valueSum

    count = 0
    key2Title2MaxMinDiffMapMap = {}
    for i in range(len(idxList)):
        key = idxList[i]
        print("xxx key =", key)
        if pltIdxMap[key] == 1:
            title2MaxMinDiffMap = pltAccAverAll(fileIDList, fileID2RMap, fileID2DsMap, fileID2Idx2AverageAccMap, fw2Plt,
                                                key, count, nRow,
                                                nCol,
                                                isLegend, isPltFill)
            key2Title2MaxMinDiffMapMap[key] = title2MaxMinDiffMap
            count += 1
    return key2Title2MaxMinDiffMapMap


def getGenPltInput():
    fw2Plt = [
        ["Ours-0.85", "purple", 3, "-", 0.6],
    ]

    fileIDListInput = [
        ['20250716104534_037397', ''],  # M_beta0.3_Ours0.85, GEN
        ['20250714220558_043397', ''],  # M_beta0.3_0.85, Gen, saved
        ['20250715101843_084484', ''],  # M_beta0.3_0.85, Pub, saved

        ['20250622000033_074801', ''],  # L
        ['20250716004043_061963', ''],  # L
    ]
    return fw2Plt, fileIDListInput


def getPltExpInput(pltIndex):
    oursPlt, benchmarkPlt = getPltInfor()
    if pltIndex == 0:
        fw2Plt, fileIDListInput = getExpFileIDAll(oursPlt, benchmarkPlt)
    elif pltIndex == 1:
        fw2Plt, fileIDListInput = getExpFileIDJustOurs(oursPlt)
    else:
        fw2Plt, fileIDListInput = getExpFileIDJustBenchmarks(benchmarkPlt)
    return fw2Plt, fileIDListInput


def getPltInfor():
    oursPlt = [
        ["Ours-0.65", "red", 5.5, "-", 0.5],
        ["Ours-0.70", "yellow", 5.5, "-", 0.5],
        ["Ours-0.75", "blue", 5.5, "-", 0.5],
        ["Ours-0.80", "green", 5.5, "-", 0.5],
        ["Ours-0.85", "cyan", 5.5, "-", 0.5],
        ["Ours-0.90", "purple", 5.5, "-", 0.5],
    ]

    benchmarkPlt = [
        ["FedAPEN", "k", 1, "-", 1.0],
        ["FedTGP", "k", 1, "-", 1.0],
        ["Cronus", "k", 1, "-", 1.0],
        ["FedDF", "k", 1, "-", 1.0],
        ["FedProto", "k", 1, "-", 1.0],
        # ["FedGEMS", "black", 1, "-", 1.0],
        ["FedMD", "blue", 1, "-", 1.0],
        ["FedProx", "k", 1, "-", 1.0],
        ["FedAvg", "k", 1, "-", 1.0]
    ]
    return oursPlt, benchmarkPlt


# def getPltInfor():
#     oursPlt = [
#         ["Ours-0.65", "red", 5.5, "-", 0.5],
#         ["Ours-0.70", "yellow", 5.5, "-", 0.5],
#         ["Ours-0.75", "blue", 5.5, "-", 0.5],
#         ["Ours-0.80", "green", 5.5, "-", 0.5],
#         ["Ours-0.85", "cyan", 5.5, "-", 0.5],
#         ["Ours-0.90", "purple", 5.5, "-", 0.5],
#     ]
#
#     benchmarkPlt = [
#         ["FedAPEN", "red", 1, "-", 1.0],
#         ["FedTGP", "yellow", 1, "-", 1.0],
#         ["Cronus", "blue", 1, "-", 1.0],
#         ["FedDF", "green", 1, "-", 1.0],
#         ["FedProto", "violet", 1, "-", 1.0],
#         # ["FedGEMS", "black", 1, "-", 1.0],
#         ["FedMD", "cyan", 3, "-", 1.0],
#         ["FedProx", "purple", 1, "-", 1.0],
#         ["FedAvg", "tomato", 1, "-", 1.0]
#     ]
#     return oursPlt, benchmarkPlt


def getExpFileIDAll(oursPlt, benchmarkPlt):
    fw2Plt = oursPlt + benchmarkPlt

    fileIDListInput = [
        ['20250616190753_050361', ''],  # M_0.1 (15 fw) # FedGEMS is wrong
        ['20250618141254_025423', ''],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
        ['20250620220350_018565', ''],  # L_0.1_50data, (0Ours, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        ['20250618142044_000804', ''],  # B_0.1 (15 fw) + run Cronus
        ['20250618143322_034012', ''],  # K_0.1 (15 fw), + run Cronus

        ['20250619111335_018997', ''],  # M_0.3 (15 fw)
        ['20250619111551_013657', ''],  # S_0.3 (15 fw) + run Cronus
        ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 3FedDF, 6FedProto, 8FedProx, 9FedAvg)
        ['20250619160516_027627', ''],  # B_0.3 (15 fw) + run Cronus
        ['20250619111744_055767', ''],  # K_0.3 (15 fw), + run Cronus

        ['20250712131126_091915', '-'],  # B_0.5_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
        ['20250711215000_096563', '-'],  # B_0.7_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
        ['20250712003058_080632', '-'],  # B_0.9_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved

        ['20250713234603_083070', '-'],  # K_0.5_Ours, saved
        ['20250713235053_091597', '-'],  # K_0.7_Ours, saved
        ['20250713235249_007780', '-'],  # K_0.9_Ours, saved

        ['20250624095904_078609', '-'],  # M_0.1_65-70-75-80-85-90 (added)
        ['20250621151912_083574', '-'],  # M_0.3_65-70-75-80-85-90 (added)

        ['20250624140511_099715', '-'],  # S_0.1_65-70-75-80-85-90 (added)
        ['20250624233644_021352', '-'],  # S_0.3_65-70-75-80-85-90 (added)

        ['20250625231904_057633', '-'],  # L_0.1_65-70-75
        ['20250625224910_012705', '-'],  # L_0.3_65-70 (running)

        ['20250623211522_087167', '-'],  # B_0.1_65-70-75-80-85-90 (added)
        ['20250621081442_055955', '-'],  # B_0.3_65-70-75-80-85-90 (added)

        ['20250623212407_065360', '-'],  # K_0.1_65-70-75-80-85-90 (added)
        ['20250621075843_084608', '-'],  # K_0.3_65-70-75-80-85-90 (added)
    ]
    return fw2Plt, fileIDListInput


def pltConf(iterNum, clientNum, eachClientIterRadarLisMap):
    for iterIdx in range(2, iterNum + 1):
        for clientIndex in range(1, clientNum + 1):
            plt.subplot(iterNum, clientNum, (iterIdx - 2) * clientNum + clientIndex)
            plt.plot(eachClientIterRadarLisMap[str(iterIdx) + "-" + str(clientIndex)], color="k", linestyle="--",
                     alpha=0.5, linewidth=3, label="Ours")
            plt.ylim(0, 1)


def ifOneValue(v):
    return len(set(v[-10:])) == 1


def pltTwoLinesIDGenPubCompare(fileID2Idx2AverageAccMap):
    plt.subplot(1, 1, 1)
    # L
    # plt.subplot(1, 2, 2)
    vL1 = fileID2Idx2AverageAccMap['20250622000033_074801'][14]  # Pub
    vL2 = fileID2Idx2AverageAccMap['20250716004043_061963'][0]  # Gen
    plt.plot(vL1, 'blue', linewidth=3, label="LC25000-Public", linestyle="-", alpha=0.65)
    plt.plot(vL2, 'blue', linewidth=3, label="LC25000-Generated", linestyle="--", alpha=0.95)

    # M
    vM1 = fileID2Idx2AverageAccMap['20250715101843_084484'][0]  # Pub
    vM2 = fileID2Idx2AverageAccMap['20250714220558_043397'][0]  # Gen
    plt.plot(vM1[:len(vL1)], 'k', linewidth=3, label="MNIST-Public", linestyle="-", alpha=0.65)
    plt.plot(vM2[:len(vL1)], 'k', linewidth=3, label="MNIST-Generated", linestyle="--", alpha=0.95)
    # plt.title("M Gen And Pub", fontsize=16)
    # plt.ylim(0, 120)
    # plt.legend()

    plt.xlabel("Iteration", fontsize=22)
    plt.ylabel("Acc", fontsize=22)

    # plt.title("Comparison of Different Approach for Building the Proxy Dataset", fontsize=18)
    plt.ylim(40, 120)
    plt.legend()

    plt.show()


# def pltTwoLinesIDGenPubCompare(fileID2Idx2AverageAccMap):
#     plt.subplot(1, 2, 1)
#     # M
#     v1 = fileID2Idx2AverageAccMap['20250715101843_084484'][0]  # Pub
#     v2 = fileID2Idx2AverageAccMap['20250714220558_043397'][0]  # Gen
#     plt.plot(v1, 'darkblue', linewidth=5, label="Pub")
#     plt.plot(v2, 'lightblue', linewidth=5, label="Gen")
#     plt.title("M Gen And Pub", fontsize=16)
#     plt.ylim(40, 120)
#     plt.legend()
#
#     # L
#     # plt.subplot(1, 2, 2)
#     v1 = fileID2Idx2AverageAccMap['20250622000033_074801'][14]  # Pub
#     v2 = fileID2Idx2AverageAccMap['20250716004043_061963'][0]  # Gen
#     plt.plot(v1, 'darkblue', linewidth=5, label="Pub")
#     plt.plot(v2, 'lightblue', linewidth=5, label="Gen")
#     plt.title("L Gen And Pub", fontsize=16)
#     plt.ylim(40, 120)
#     plt.legend()
#
#     plt.show()

def getCentralTrainResult():
    m = [
        ['20250616190753_050361', 0.975, 0.975],
        ['20250618141254_025423', 0.968, 0.961],
        ['20250620220350_018565', 0.979, 0.979],
        ['20250618142044_000804', 0.931, 0.928],
        ['20250618143322_034012', 0.773, 0.784],

        ['20250619111335_018997', 0.978, 0.978],
        ['20250619111551_013657', 0.967, 0.963],
        ['20250622000033_074801', 0.989, 0.989],
        ['20250619160516_027627', 0.953, 0.954],
        ['20250619111744_055767', 0.769, 0.775]
    ]

    mapAll = {}
    for v in m:
        for resultName in ['acc', 'maf1']:
            mapAll[v[0] + "-" + resultName] = v[1 + ['acc', 'maf1'].index(resultName)]

    s = 'Central Training & '
    idx = 1
    for i in range(5):
        s += str(m[i][idx]) + " & " + str(m[i + 5][idx]) + " & "
    s = s[: -3] + " \\\\"
    print(s)

    s = 'Central Training & '
    idx = 2
    for i in range(5):
        s += str(m[i][idx]) + " & " + str(m[i + 5][idx]) + " & "
    s = s[: -3] + " \\\\"
    print(s)

    return mapAll


def pltAccAverAll(fileIDList, fileID2RMap, fileID2DsMap, fileID2Idx2AverageAccMap, fw2Plt, idxKW, addIdx, nRow, nCol,
                  isLegend, isPltFill):
    mapAllCentralResult = getCentralTrainResult()

    fwPltList = []
    for v in fw2Plt:
        fwPltList.append(v[0])

    title2MaxMinDiffMap = {}

    for fileID in fileIDList:
        print("xxx fileID =", fileID)
        print("xxx idxKW =", idxKW)
        thisCentralResult = mapAllCentralResult[fileID + "-" + idxKW]

        plt.subplot(nRow, nCol, fileIDList.index(fileID) + 1 + len(fileIDList) * addIdx)
        iterLength = None
        ##################################################################################################
        maxAccSum, minAccSum = 0, 10000000
        maxIdx, minIdx = 0, 0

        maxAccSumOurs, maxIdxOurs = 0, 0
        ##################################################################################################
        countPltN = 0

        benchmarkAccList = []
        for idx in fileID2Idx2AverageAccMap[fileID].keys():
            thisAccList = fileID2Idx2AverageAccMap[fileID][idx]
            thisFwName = fileID2RMap[fileID]['MapFramework'][int(fileID2RMap[fileID]['idx2Exp'][idx][0])]
            if fileID2RMap[fileID]['idx2Exp'][idx][1] != "None":
                thisFwName += "-" + fileID2RMap[fileID]['idx2Exp'][idx][1]
            if thisFwName in fwPltList:
                ################################################################################################
                if thisFwName.__contains__("Ours"):
                    if sum(thisAccList[-3:]) > maxAccSumOurs:
                        maxAccSumOurs = sum(thisAccList[-3:])
                        maxIdxOurs = idx
                ################################################################################################
                if sum(thisAccList) > maxAccSum:
                    maxAccSum = sum(thisAccList)
                    maxIdx = idx
                if sum(thisAccList) < minAccSum:
                    minAccSum = sum(thisAccList)
                    minIdx = idx
                ################################################################################################
                thisColor = getValueFromList(fw2Plt, thisFwName, 0)
                thisLineWidth = getValueFromList(fw2Plt, thisFwName, 1)
                thisLineStyle = getValueFromList(fw2Plt, thisFwName, 2)
                thisAlpha = getValueFromList(fw2Plt, thisFwName, 3)
                iterLength = len(thisAccList)

                if ifOneValue(thisAccList):
                    thisLineWidth += 3
                    thisLineStyle = ':'
                countPltN += 1
                # print("thisFwName =", thisFwName)
                if not thisFwName.__contains__("Ours"):
                    # thisColor = 'k'
                    # if thisFwName.__contains__("FedMD"):
                    #     thisColor = 'b'
                    # if thisFwName.__contains__("Ours"):
                    # if True:
                    benchmarkAccList.append(sum(thisAccList[-3:])/3)
                    plt.plot(
                        thisAccList,
                        color=thisColor,
                        linestyle=thisLineStyle,
                        alpha=thisAlpha,
                        linewidth=thisLineWidth,
                        label=thisFwName
                    )
        ################################################################################################
        thisAccListMax = fileID2Idx2AverageAccMap[fileID][maxIdxOurs]
        print("benchmarkAccList, thisAccListMax, thisCentralResult=", benchmarkAccList, sum(thisAccListMax[-3:])/3, thisCentralResult)
        avg1 = sum(benchmarkAccList)/len(benchmarkAccList)
        avg2 = sum(thisAccListMax[-3:])/3
        #print("avg benchmarkAccList, thisAccListMax, thisCentralResult=", benchmarkAccList, avg1, avg2, thisCentralResult * 100,
        #     1-(thisCentralResult * 100 - avg2)/(thisCentralResult * 100 - avg1))
        #print("avg benchmarkAccList, thisAccListMax, thisCentralResult=", 1 - (thisCentralResult * 100 - avg2) / (thisCentralResult * 100 - avg1))
        ##########################################################################
        if thisFwName.__contains__("Ours"):
            thisFwNameNew = "FedADC"
        ##########################################################################

        plt.plot(
            thisAccListMax,
            # color="brown",
            color="darkblue",
            linestyle=thisLineStyle,
            alpha=0.9,
            linewidth=3.5,
            label=thisFwNameNew
        )
        plt.plot(
            [thisCentralResult * 100] * len(thisAccListMax),
            # color="brown",
            color="grey",
            linestyle='--',
            alpha=1.0,
            linewidth=1.5,
            label="Central Training"
        )
        ################################################################################################
        diffMaxMin = None
        if countPltN > 1 and isPltFill:
            print("fileID maxIdx, minIdx", fileID, maxIdx, minIdx)
            thisAccListMax = fileID2Idx2AverageAccMap[fileID][maxIdxOurs]
            thisAccListMin = fileID2Idx2AverageAccMap[fileID][minIdx]
            # print("thisAccListMax =", thisAccListMax)
            # print("thisAccListMin =", thisAccListMin)
            ##############################################################################################
            diffMaxMin = thisAccListMax[-1] - thisAccListMin[-1]
            ##############################################################################################
            plt.fill_between(list(range(len(thisAccListMax))), thisAccListMin, thisAccListMax, facecolor='gray',
                             alpha=0.7)
        ################################################################################################
        # plt.plot([fileID2DsMap[fileID][idxKW]] * iterLength, color="k", linestyle="--", alpha=0.5, linewidth=1.5,
        #          label="CentralTrain")
        ################################################################################################
        if idxKW == "maf1":
            idxKWNew = "Macro-F1"
        if idxKW == "acc":
            idxKWNew = "Acc"
        ################################################################################################
        # plt.xlabel('Iteration', fontsize=8, color='k')
        # print("xxx", fileIDList.index(fileID) + 1 + len(fileIDList) * addIdx, nCol, (fileIDList.index(fileID) + 1 + len(fileIDList) * addIdx) % nCol)
        if (fileIDList.index(fileID) + 1 + len(fileIDList) * addIdx) % nCol == 1:
            plt.ylabel(idxKWNew, fontsize=10, color='k')
        plt.ylim(0, 105)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.title(dealWithTitle(fileID2RMap[fileID]["thisTitle"]), fontsize=10)
        title2MaxMinDiffMap[fileID2RMap[fileID]["thisTitle"]] = diffMaxMin

        # if isLegend and fileIDList.index(fileID) == len(fileIDList) - 1:
        # if isLegend and fileIDList.index(fileID) == 0:
        if isLegend:
            plt.legend(fontsize=4)

        # plt.grid()
    plt.show()

    return title2MaxMinDiffMap


def dealWithTitle(titleInput):
    m = {
        'mnist': 'MNIST',
        'sate': 'Satellite Image',
        'lc': 'LC25000',
        'btumor': 'Btumor',
        'knee': 'KOA'
    }
    v = titleInput.split("-")
    a = m[v[0]]
    b = v[1]
    return a + "-" + b


def getAllClientsAverageAccMap(eachClient2AccListMap):
    averageAccList = []
    for i in range(len(eachClient2AccListMap[1])):
        s = 0
        for clientIndex in range(1, len(eachClient2AccListMap) + 1):
            s += eachClient2AccListMap[clientIndex][i]
        s = s / len(eachClient2AccListMap)
        averageAccList.append(s)
    return averageAccList


def getEachClient2AccListMap(fileID, idx, rMap, kw):
    fileName = "D:/FedAD/FedXXX/OutputResult/" + fileID + "/Result_" + fileID + "_" + str(idx) + ".txt"
    if not os.path.exists(fileName):
        return None
    ###############################################################
    iterStartMap = {"acc": 1, "maf1": 1, "mif1": 1, "radar": 2}
    # iterStartMap = {"acc": 2, "maf1": 2, "mif1": 2, "radar": 2}
    ###############################################################
    eachClientIterAccLisMap = {}
    with open(fileName, 'r') as file:
        content = file.read()
        for line in content.split("\n"):
            if line.__contains__(kw):
                eachClientIterAccLisMap[line.split("-")[1] + "-" + line.split("-")[2]] = tranStr2Float100List(
                    line.split("-")[3][1: -1].split(", "))
                # if kw != "radar":
                #     eachClientIterAccLisMap[line.split("-")[1] + "-" + line.split("-")[2]] = tranStr2Float100List(
                #         line.split("-")[3][1: -1].split(", "))
                # else:
                #     eachClientIterAccLisMap[line.split("-")[1] + "-" + line.split("-")[2]] = tranStr2Float100List(
                #         line.split("-")[3][1: -1].split(", "))
    eachClient2AccListMap = None
    if len(eachClientIterAccLisMap) > 0:
        eachClient2AccListMap = {}
        for clientIndex in range(1, rMap["clientNum"] + 1):
            accList = []
            for iterIndex in range(iterStartMap[kw], rMap["iterNum"] + 1):
                accList += eachClientIterAccLisMap[str(iterIndex) + "-" + str(clientIndex)]
            eachClient2AccListMap[clientIndex] = accList
    return eachClient2AccListMap


def smoothL(L):
    N = 2
    newL = L[: N]
    for i in range(N, len(L) - N):
        newL.append(sum(L[i - N: i + N + 1]) / (N * 2 + 1))
    newL += L[-N:]
    return newL


def getFileIDList(fileIDListInput):
    fileIDList = []
    for v in fileIDListInput:
        if v[1] == '':
            fileIDList.append(v[0])
    return fileIDList


def getEachIterStuTeaRelationship(fileID):
    idx2Iter2RShipMap = {}
    for idx in [0, 10, 11, 12, 13, 14]:
        fileName = "D:/FedAD/FedXXX/OutputResult/" + fileID + "/Result_" + fileID + "_" + str(idx) + ".txt"

        if not os.path.exists(fileName):
            return None

        iter2RShipMap = {}
        with open(fileName, 'r') as file:
            content = file.read()
            for line in content.split("\n"):
                if line.__contains__("thisOuterEachClient2TeacherMap"):
                    iter2RShipMap[
                        int(line.split("outIter = ")[1].split(" thisOuterEachClient2TeacherMap")[
                                0])] = ast.literal_eval(
                        line.split(" thisOuterEachClient2TeacherMap = ")[1])
        idx2Iter2RShipMap[idx] = iter2RShipMap
    return idx2Iter2RShipMap


def getBoldSet(dataNameList, nonIIDList, tableMapAccMaf1Mif1, nonIIDParameterMap):
    boldKeySetAcc, boldKeySetMaf1, boldKeySetMif1 = set(), set(), set()
    for dataName in dataNameList:
        for nonIID in nonIIDList:
            maxAccKey, maxAcc = None, -1
            maxMaf1Key, maxMaf1 = None, -1
            maxMif1Key, maxMif1 = None, -1
            for key in tableMapAccMaf1Mif1:
                keySplit = key.split("-")
                if keySplit[0] == dataName and keySplit[-1] == str(nonIIDParameterMap[nonIID]):
                    thisAcc = float(tableMapAccMaf1Mif1[key][0])
                    thisMaf1 = float(tableMapAccMaf1Mif1[key][1])
                    thisMif1 = float(tableMapAccMaf1Mif1[key][2])
                    if thisAcc >= maxAcc:
                        maxAcc = thisAcc
                        maxAccKey = key
                    if thisMaf1 >= maxMaf1:
                        maxMaf1 = thisMaf1
                        maxMaf1Key = key
                    if thisMif1 >= maxMif1:
                        maxMif1 = thisMif1
                        maxMif1Key = key
            boldKeySetAcc.add(maxAccKey)
            boldKeySetMaf1.add(maxMaf1Key)
            boldKeySetMif1.add(maxMif1Key)
    return boldKeySetAcc, boldKeySetMaf1, boldKeySetMif1


def getOneRowTable(resultIdx, s, fwListAll, dataNameList, nonIIDList, tableMapAccMaf1Mif1, nonIIDParameterMap,
                   boldKeySetXXX):
    ifLineAdded = False
    for fw in fwListAll:
        if fw.__contains__("Ours") and ifLineAdded is False:
            s.append("\\" + "cmidrule(r){1-11}")
            ifLineAdded = True
        if fw == "Ours":
            oneRow = "\\" + "textbf{" + fw + "}" + " & "
        else:
            oneRow = fw + " & "
        for dataName in dataNameList:
            for nonIID in nonIIDList:
                thisKey = dataName + "-" + fw + "-" + str(nonIIDParameterMap[nonIID])
                if thisKey in tableMapAccMaf1Mif1.keys():
                    # if fw == "Ours":
                    if thisKey in boldKeySetXXX:
                        oneRow += "\\" + "textbf{" + "\\" + "underline{" + tableMapAccMaf1Mif1[thisKey][
                            resultIdx] + "}" + "}" + " & "
                    else:
                        oneRow += tableMapAccMaf1Mif1[thisKey][resultIdx] + " & "
                else:
                    if fw == "Ours":
                        oneRow += "\\" + "textbf{X}" + " & "
                    else:
                        oneRow += "X" + " & "
        s.append(oneRow[: -2] + "\\\\")


def resultsTable(
        fileIDList,
        fileID2Idx2Client2AccListMapMap, fileID2RMap,
        fileID2Idx2AccMap, fileID2Idx2Maf1Map, fileID2Idx2Mif1Map
):
    tableMapAccMaf1Mif1 = {}
    for fileID in fileIDList:
        for idx in fileID2Idx2Client2AccListMapMap[fileID].keys():
            thisFwName = fileID2RMap[fileID]['MapFramework'][int(fileID2RMap[fileID]['idx2Exp'][idx][0])]
            if fileID2RMap[fileID]['idx2Exp'][idx][1] != "None":
                thisFwName += "-" + fileID2RMap[fileID]['idx2Exp'][idx][1]
            thisKey = fileID2RMap[fileID]['dataNameMap'][
                          fileID2RMap[fileID]['dataName']] + "-" + thisFwName + "-" + str(
                fileID2RMap[fileID]['dirichletAlpha'])
            tableMapAccMaf1Mif1[thisKey] = [
                str(round(fileID2Idx2AccMap[fileID][idx], 2)),
                str(round(fileID2Idx2Maf1Map[fileID][idx], 2)),
                str(round(fileID2Idx2Mif1Map[fileID][idx], 2))
            ]
    return tableMapAccMaf1Mif1


def getTable(s, idxName, resultName2IdxMap, dataNameList, nonIIDList, fw2Plt, tableMapAccMaf1Mif1, nonIIDParameterMap,
             boldKeySetXXX):
    resultIdx = resultName2IdxMap[idxName]

    fwListAll = []
    for i in range(len(fw2Plt)):
        fwListAll.append(fw2Plt[len(fw2Plt) - 1 - i][0])

    colNumTable = len(dataNameList) * len(nonIIDList)
    colWidth = 15
    ######################################################################################################################
    a1 = ""
    for i in range(colNumTable):
        a1 += "p{" + str(colWidth) + "mm}"
    a1 += "}"

    a2 = ""
    for dataName in dataNameList:
        a2 += "multicolumn{" + str(len(nonIIDList)) + "}{c}{" + "\\" + "textbf{" + dataName + "}}" + "&" + "\\"
    a2 = a2[:-2] + " \\\\"

    a3 = ""
    for i in range(len(dataNameList)):
        a3 += "\\" + "cmidrule(r){" + str(2 + i * len(nonIIDList)) + "-" + str(1 + (i + 1) * len(nonIIDList)) + "}"
    for i in range(len(dataNameList)):
        for nonIIDName in nonIIDList:
            a3 += " & " + nonIIDName
    a3 += " \\\\"
    ######################################################################################################################
    s.append("\\" + "\\")
    s.append("   ")
    s.append("The following table is the " + idxName + " results:" + "\\" + "\\")
    s.append("\\" + "begin{adjustbox}{width=0.85" + "\\" + "textwidth}")
    s.append("\\" + "renewcommand{" + "\\" + "arraystretch}{1.5}")
    s.append("\\" +
             "begin{tabular}{p{" + str(colWidth) + "mm}" + a1
             )
    s.append("\\" + "toprule")
    s.append("\\" + "cmidrule(r){1-" + str(1 + colNumTable) + "}")
    s.append("\\" + "multirow{" + str(
        len(nonIIDList)) + "}{1cm}{" + "\\" + "centering " + "\\" + "textbf{Method}}&" + "\\" + a2)
    s.append(a3)
    s.append("\\" + "cmidrule(r){1-" + str(1 + colNumTable) + "}")
    getOneRowTable(resultIdx, s, fwListAll, dataNameList, nonIIDList, tableMapAccMaf1Mif1, nonIIDParameterMap,
                   boldKeySetXXX)
    s.append("\\" + "bottomrule")
    s.append("\\" + "end{tabular}")
    s.append("\\" + "end{adjustbox}")


def pltAccAll(fileIDList, fileID2RMap, fileID2DsMap, fileID2Idx2Client2AccListMapMap, fw2Plt, idxKW, isLegend):
    fwPltList = []
    for v in fw2Plt:
        fwPltList.append(v[0])

    for fileID in fileIDList:
        for clientIndex in range(1, fileID2RMap[fileID]["clientNum"] + 1):
            plt.subplot(len(fileIDList), fileID2RMap[fileID]["clientNum"],
                        fileIDList.index(fileID) * fileID2RMap[fileID]["clientNum"] + clientIndex)
            iterLength = None
            for idx in fileID2Idx2Client2AccListMapMap[fileID].keys():
                thisAccList = fileID2Idx2Client2AccListMapMap[fileID][idx][clientIndex]
                thisFwName = fileID2RMap[fileID]['MapFramework'][int(fileID2RMap[fileID]['idx2Exp'][idx][0])]
                if fileID2RMap[fileID]['idx2Exp'][idx][1] != "None":
                    thisFwName += "-" + fileID2RMap[fileID]['idx2Exp'][idx][1]
                if thisFwName in fwPltList:
                    thisColor = getValueFromList(fw2Plt, thisFwName, 0)
                    thisLineWidth = getValueFromList(fw2Plt, thisFwName, 1)
                    thisLineStyle = getValueFromList(fw2Plt, thisFwName, 2)
                    thisAlpha = getValueFromList(fw2Plt, thisFwName, 3)
                    iterLength = len(thisAccList)

                    if ifOneValue(thisAccList):
                        thisLineWidth += 3
                        thisLineStyle = ':'

                    plt.plot(
                        thisAccList,
                        color=thisColor,
                        linestyle=thisLineStyle,
                        alpha=thisAlpha,
                        linewidth=thisLineWidth,
                        label=thisFwName
                    )

            plt.plot([fileID2DsMap[fileID][idxKW]] * iterLength, color="k", linestyle="--", alpha=0.5,
                     linewidth=3, label="CentralTrain")
            plt.ylim(0, 100)
            plt.xlabel('Iteration', fontsize=14, color='k')
            plt.ylabel(idxKW, fontsize=14, color='k')
            plt.title(fileID2RMap[fileID]["thisTitle"] + " Client" + str(clientIndex))

            if isLegend:
                plt.legend()

            plt.grid()
    plt.show()


def getEachClient2ConfListMap(fileID):
    expIndex = 0
    fileName = "D:/FedAD/FedXXX/OutputResult/" + fileID + "/Result_" + fileID + "_" + str(expIndex) + ".txt"

    if not os.path.exists(fileName):
        return None

    eachClientIterRadarLisMap = {}
    with open(fileName, 'r') as file:
        content = file.read()
        for line in content.split("\n"):
            if line.__contains__("radar"):
                eachClientIterRadarLisMap[line.split("-")[1] + "-" + line.split("-")[2]] = tranStr2Float100List(
                    line.split("-")[3][1: -1].split(", "))

    return eachClientIterRadarLisMap


def getFilenamesInFolder(folderPath):
    filenames = []
    for filename in os.listdir(folderPath):
        if os.path.isfile(os.path.join(folderPath, filename)):
            filenames.append(filename)
    return filenames


def getTeacherFreTotalMap(fileID, fileID2Iter2RShipMapInput, idxInput):
    iterNum = len(fileID2Iter2RShipMapInput[fileID][idxInput])
    teacherFreTotalMap = {}
    maxPtList = []
    for iterUsed in range(2, iterNum + 2):
        teacherFreMap = {}
        thisIterMap = fileID2Iter2RShipMapInput[fileID][idxInput][iterUsed]
        for pt in thisIterMap.keys():
            thisTeacher = thisIterMap[pt]
            if thisTeacher not in teacherFreMap.keys():
                teacherFreMap[thisTeacher] = 0
            teacherFreMap[thisTeacher] += 1

        maxFre, maxPt = -1, 0
        for pt in teacherFreMap.keys():
            if teacherFreMap[pt] > maxFre:
                maxFre = teacherFreMap[pt]
                maxPt = pt
            if pt not in teacherFreTotalMap.keys():
                teacherFreTotalMap[pt] = 0
            teacherFreTotalMap[pt] += teacherFreMap[pt]
        maxPtList.append(maxPt)

    print("teacherFreTotalMap =", teacherFreTotalMap)
    return teacherFreTotalMap, maxPtList


def pltClientStuTea(titleInput, fileID2RMap, fileID2Iter2RShipMapInput, idxInput, fileID, rN, cN, pColor, linkColor,
                    azInput):
    pNum = fileID2RMap[fileID]["clientNum"]

    iterNum = len(fileID2Iter2RShipMapInput[fileID][idxInput])

    colors = [pColor] * pNum

    fig, ax = plt.subplots(rN, cN, figsize=(12, 12))

    for iterUsed in range(2, iterNum + 2):
        DG = nx.DiGraph()

        v = []
        for i in range(pNum):
            v.append("C" + str(i + 1))
        DG.add_nodes_from(v)

        vv = []
        teacherFreMap = {}
        thisIterMap = fileID2Iter2RShipMapInput[fileID][idxInput][iterUsed]
        for pt in thisIterMap.keys():
            thisTeacher = thisIterMap[pt]
            vv.append(("C" + str(thisTeacher), "C" + str(pt)))
            if thisTeacher not in teacherFreMap.keys():
                teacherFreMap[thisTeacher] = 0
            teacherFreMap[thisTeacher] += 1

        #####################################################################
        ptSizeList = [800] * pNum
        #####################################################################
        # ptSizeList = []
        # for pt in range(1, pNum + 1):
        #     if pt in teacherFreMap.keys():
        #         ptSizeList.append(200 + teacherFreMap[pt] * 350)
        #     else:
        #         ptSizeList.append(200)
        #####################################################################

        DG.add_edges_from(vv)

        pos = nx.circular_layout(DG)

        plt.subplot(rN, cN, iterUsed - 1)
        nx.draw(DG, pos=pos, with_labels=True,
                node_color=colors, edge_color=linkColor, node_size=ptSizeList,
                font_size=10, width=1, font_color='white', alpha=1.0, arrowstyle='-|>',
                connectionstyle='Arc3, rad=-0.3', arrowsize=azInput
                # style='dashed'
                )
        plt.title("Iter Num = " + str(iterUsed))
    fig.suptitle(titleInput, fontsize=20, fontweight='bold')
    # fig.suptitle('xxx', x=0.5, y=0.95, fontsize=14, fontweight='bold', color='red')
    plt.show()


def getIdxListList(fileID2RMap, fileID2DsMap, fileID):
    iterNum, labelNum = fileID2RMap[fileID]["iterNum"], fileID2DsMap[fileID]["labelNum"]
    idxListList = []
    for i in range(iterNum - 1):
        idxListList.append([i * labelNum, (i + 1) * labelNum])
    return idxListList


def getFileID2LabelNameMap(fileIDList, fileID2RMap):
    fileID2LabelNamesMap = {}
    fileID2TrainTestDataNumSizeMap = {}
    for fileID in fileIDList:
        concatDataset, className = getData(fileID2RMap[fileID]['dataName'])
        fileID2LabelNamesMap[fileID] = className
        ###############################################################################################
        if fileID2RMap[fileID]['dataName'] in ["C", "L"]:
            p = 0.5
        else:
            p = 1
        ###############################################################################################
        fileID2TrainTestDataNumSizeMap[fileID] = [fileID2RMap[fileID]['dataName'], int(len(concatDataset) * p * 0.7),
                                                  int(len(concatDataset) * p * 0.3), concatDataset[0][0].shape,
                                                  len(concatDataset.classes)]
    return fileID2LabelNamesMap, fileID2TrainTestDataNumSizeMap


def getInforFromGenFile(fileID):
    with open("D:/FedAD/FedXXX/OutputResult/" + fileID + "/GenExp_" + fileID + ".txt", 'r') as file:
        content = file.read()
        ##############################################################################
        dataNameMap = None
        dataDisNameMap = None
        MapFramework = None

        clientNum = None
        iterNum = None
        expNum = 0
        dataName = None

        idx2Exp = {}

        dirichletAlpha = None
        thisLr = None

        thisTitle = ""
        ##############################################################################
        for thisLine in content.split("\n"):
            if len(thisLine) > 0 and thisLine[0] == "#":
                continue
            ##############################################################################
            if thisLine.__contains__("MapDataName"):
                dataNameMap = ast.literal_eval(thisLine.split("MapDataName-")[1])
            if thisLine.__contains__("MapDataDis"):
                dataDisNameMap = ast.literal_eval(thisLine.split("MapDataDis-")[1])
            if thisLine.__contains__("MapFramework"):
                MapFramework = ast.literal_eval(thisLine.split("MapFramework-")[1])
            ##############################################################################
            if thisLine.__contains__("clientNum"):
                clientNum = int(thisLine.split("clientNum: ")[1])
            if thisLine.__contains__("outIterNum"):
                iterNum = int(thisLine.split("outIterNum: ")[1])
            if thisLine.__contains__("testExpSet"):
                expNum += 1
                idx2Exp[int(thisLine.split("testExpSet-")[1].split(": ")[0])] = thisLine.split(": ")[1].split(", ")
            if thisLine.__contains__("thisLr"):
                thisLr = float(thisLine.split("thisLr: ")[1])
            ##############################################################################
            if thisLine.__contains__("expName"):
                dataName = thisLine.split("expName: ")[1]
                thisTitle += dataNameMap[dataName]
            if thisLine.__contains__("useNormalizeOrDirichlet"):
                # thisTitle += "-" + dataDisNameMap[thisLine.split("useNormalizeOrDirichlet: ")[1]]
                dataDisName = thisLine.split("useNormalizeOrDirichlet: ")[1]
            if thisLine.__contains__("dirichletAlpha") and dataDisName == "D":
                dirichletAlpha = float(thisLine.split("dirichletAlpha: ")[1])
                thisTitle += "-" + str(dirichletAlpha)
            ##############################################################################
    rMap = {
        "dataName": dataName,
        "dirichletAlpha": dirichletAlpha,
        "thisTitle": thisTitle,
        "expNum": expNum,
        "idx2Exp": idx2Exp,
        "iterNum": iterNum,
        "clientNum": clientNum,
        "thisLr": thisLr,
        "dataNameMap": dataNameMap,
        "dataDisNameMap": dataDisNameMap,
        "MapFramework": MapFramework
    }
    return rMap


# def getTableAccInforMap(fileIDList):
#     tableAccInforMap = {}
#     for fileID in fileIDList:
#         rMap = getInforFromGenFile(fileID)
#         eachClient2AccListMapList = getEachClient2AccListMapList(fileID, expNum, iterNum, clientNum)
#         eachFramework2AccMap = getEachFramework2AccMap(expNum, MapFramework, eachClient2AccListMapList)
#         for fwName in eachFramework2AccMap.keys():
#             thisKey = thisTitle + "-" + fwName
#             if thisKey not in tableAccInforMap.keys():
#                 tableAccInforMap[thisKey] = []
#             tableAccInforMap[thisKey].append(eachFramework2AccMap[fwName])
#     return tableAccInforMap


def getLabelDis(labelNum, indexClientLabel2NumMap):
    labelDistribution = []
    for labelIndex in range(labelNum):
        labelDistribution.append([])

    for key in indexClientLabel2NumMap.keys():
        thisClient = int(key.split("-")[0])
        thisLabel = int(key.split("-")[1])
        num = indexClientLabel2NumMap[key]
        for i in range(num):
            labelDistribution[thisLabel].append(thisClient)
    return labelDistribution


def getResultEachFileID(fileIDList, p):
    fileID2RMap = {}
    fileID2DsMap = {}

    fileID2Idx2Client2AccListMapMap = {}
    fileID2Idx2AverageAccMap = {}
    fileID2Idx2AccMap = {}

    fileID2Idx2Client2Maf1ListMapMap = {}
    fileID2Idx2AverageMaf1Map = {}
    fileID2Idx2Maf1Map = {}

    fileID2Idx2Client2Mif1ListMapMap = {}
    fileID2Idx2AverageMif1Map = {}
    fileID2Idx2Mif1Map = {}

    fileID2Idx2Client2RaListMapMap = {}

    fileID2Iter2RShipMap = {}
    for fileID in fileIDList:
        rMap, dsMap, resultIdxMap = getOneExpResult(fileID, p)

        fileID2RMap[fileID] = rMap
        fileID2DsMap[fileID] = dsMap

        fileID2Idx2Client2AccListMapMap[fileID] = resultIdxMap["idx2Client2AccListMapMap"]
        fileID2Idx2AverageAccMap[fileID] = resultIdxMap["idx2AverageAccListMap"]
        fileID2Idx2AccMap[fileID] = resultIdxMap["idx2AccMap"]

        fileID2Idx2Client2Maf1ListMapMap[fileID] = resultIdxMap["idx2Client2Maf1ListMapMap"]
        fileID2Idx2AverageMaf1Map[fileID] = resultIdxMap["idx2AverageMaf1ListMap"]
        fileID2Idx2Maf1Map[fileID] = resultIdxMap["idx2Maf1Map"]

        fileID2Idx2Client2Mif1ListMapMap[fileID] = resultIdxMap["idx2Client2Mif1ListMapMap"]
        fileID2Idx2AverageMif1Map[fileID] = resultIdxMap["idx2AverageMif1ListMap"]
        fileID2Idx2Mif1Map[fileID] = resultIdxMap["idx2Mif1Map"]

        fileID2Idx2Client2RaListMapMap[fileID] = resultIdxMap["idx2Client2RaListMapMap"]

        fileID2Iter2RShipMap[fileID] = resultIdxMap["iter2RShipMap"]

    fileIDIdxClient2RadarMap = getFileIDIdxClient2RadarMap(
        fileIDList, fileID2RMap, fileID2DsMap, fileID2Idx2Client2RaListMapMap
    )
    fileID2LabelNamesMap, fileID2TrainTestDataNumSizeMap = getFileID2LabelNameMap(fileIDList, fileID2RMap)

    return (fileID2RMap, fileID2DsMap,
            fileID2Idx2Client2AccListMapMap, fileID2Idx2AverageAccMap, fileID2Idx2AccMap,
            fileID2Idx2Client2Maf1ListMapMap, fileID2Idx2AverageMaf1Map, fileID2Idx2Maf1Map,
            fileID2Idx2Client2Mif1ListMapMap, fileID2Idx2AverageMif1Map, fileID2Idx2Mif1Map,
            fileIDIdxClient2RadarMap, fileID2Iter2RShipMap, fileID2LabelNamesMap, fileID2TrainTestDataNumSizeMap
            )


def getInforFromInpStaFile(fileID):
    pathInput = "D:/FedAD/FedXXX/OutputResult/" + fileID + "/InpSta_" + fileID + ".txt"

    indexClientLabel2NumMap = {}
    testDataLabel2NumMap = {}
    pubDataLabel2NumMap = {}

    centralAcc = None
    maf1 = None
    mif1 = None

    with open(pathInput, 'r') as file:
        labelNum = 0
        for thisLine in file.read().split("\n"):
            ###########################################################################
            if thisLine.__contains__("CentralTrain acc"):
                a = thisLine.split("CentralTrain acc = ")[1][2:-2].split("], [")
                #########################################################################
                vv = a[-1].split(", ")
                centralAcc = 100 * float(vv[0])
                maf1 = 100 * float(vv[1])
                mif1 = 100 * float(vv[2])
                #########################################################################
            ###########################################################################
            if thisLine.__contains__("TrainDataClient"):
                clientIndexStr = thisLine.split("TrainDataClient")[1].split(" count")[0]
                labelIndexStr = thisLine.split("TrainDataClient")[1].split("count ")[1].split(": ")[0]
                num = int(thisLine.split("TrainDataClient")[1].split("count ")[1].split(": ")[1])
                indexClientLabel2NumMap[clientIndexStr + "-" + labelIndexStr] = num

                if int(labelIndexStr) + 1 > labelNum:
                    labelNum = int(labelIndexStr) + 1
            ###########################################################################
            if thisLine.__contains__("TestData count") or thisLine.__contains__("pubDataTextBook count"):
                a = int(thisLine.split("count ")[1].split(":")[0])
                b = int(thisLine.split(": ")[1])
            if thisLine.__contains__("TestData count"):
                testDataLabel2NumMap[a] = b
            ###########################################################################
            if thisLine.__contains__("pubDataTextBook count"):
                pubDataLabel2NumMap[a] = b
            ###########################################################################
    dsMap = \
        {
            "indexClientLabel2NumMap": indexClientLabel2NumMap,
            "testDataLabel2NumMap": testDataLabel2NumMap,
            "pubDataLabel2NumMap": pubDataLabel2NumMap,
            "labelNum": labelNum,
            "acc": centralAcc,
            "maf1": maf1,
            "mif1": mif1
        }
    return dsMap


def cutList(v, idxListList):
    vList = []
    for idxList in idxListList:
        vList.append(v[idxList[0]: idxList[1]])
    return vList


def genLatexForOneExp(thisTitle, clientNum, labelNum, indexClientLabel2NumMap, testDataLabel2NumMap,
                      pubDataLabel2NumMap):
    sList = ["\\begin{table}[!htbp]", "\\centering", "\\label{tablename}", "\\caption{" + thisTitle + "}",
             "\\vspace{5pt}", '\\begin{tabular}{l|' + 'c' * (labelNum + 1) + '}', "\\hline"]

    s = " & "
    for labelIndex in range(labelNum):
        s += "Label " + str(labelIndex + 1) + " & "
    s += "Total" + " \\\\"
    sList.append(s)
    sList.append("\\hline")
    for clientIndex in range(1, clientNum + 1):
        s = "Client " + str(clientIndex) + " & "
        nTotal = 0
        for labelIndex in range(labelNum):
            s += str(indexClientLabel2NumMap[str(clientIndex) + "-" + str(labelIndex)]) + " & "
            nTotal += indexClientLabel2NumMap[str(clientIndex) + "-" + str(labelIndex)]
        s += str(nTotal) + " \\\\"
        sList.append(s)
    sList.append("\\hline")
    s = "TestData" + " & "
    nTotal = 0
    for labelIndex in range(labelNum):
        s += str(testDataLabel2NumMap[labelIndex]) + " & "
        nTotal += testDataLabel2NumMap[labelIndex]
    s += str(nTotal) + " \\\\"
    sList.append(s)
    sList.append("\\hline")
    s = "PubData" + " & "
    nTotal = 0
    for labelIndex in range(labelNum):
        s += str(pubDataLabel2NumMap[labelIndex]) + " & "
        nTotal += pubDataLabel2NumMap[labelIndex]
    s += str(nTotal) + " \\\\"
    sList.append(s)
    sList.append("\\hline")
    sList.append('\\end{tabular}')
    sList.append("\\end{table}")
    return sList


def getOneExpResult(fileID, p):
    rMap = getInforFromGenFile(fileID)
    dsMap = getInforFromInpStaFile(fileID)

    idx2Client2AccListMapMap, idx2Client2Maf1ListMapMap, idx2Client2Mif1ListMapMap, idx2Client2RaListMapMap = (
        getEachClient2AccListMapList(fileID, rMap))
    idx2AverageAccListMap, idx2AccMap = getEachFramework2AccMap(idx2Client2AccListMapMap, p)
    idx2AverageMaf1ListMap, idx2Maf1Map = getEachFramework2AccMap(idx2Client2Maf1ListMapMap, p)
    idx2AverageMif1ListMap, idx2Mif1Map = getEachFramework2AccMap(idx2Client2Mif1ListMapMap, p)

    idx2Iter2RShipMap = getEachIterStuTeaRelationship(fileID)

    resultIdxMap = {
        "idx2Client2AccListMapMap": idx2Client2AccListMapMap,
        "idx2AverageAccListMap": idx2AverageAccListMap, "idx2AccMap": idx2AccMap,

        "idx2Client2Maf1ListMapMap": idx2Client2Maf1ListMapMap,
        "idx2AverageMaf1ListMap": idx2AverageMaf1ListMap, "idx2Maf1Map": idx2Maf1Map,

        "idx2Client2Mif1ListMapMap": idx2Client2Mif1ListMapMap,
        "idx2AverageMif1ListMap": idx2AverageMif1ListMap, "idx2Mif1Map": idx2Mif1Map,

        "idx2Client2RaListMapMap": idx2Client2RaListMapMap,

        "iter2RShipMap": idx2Iter2RShipMap
    }

    return rMap, dsMap, resultIdxMap


def getP2LocalGoalFromOriData(fileIDStr, fileIDIdxClient2RadarMap, idx):
    path = "D:/FedAD/FedXXX/OutputResult/" + fileIDStr + "/InpSta_" + fileIDStr + ".txt"

    clientLabel2NumMap = {}
    maxNum = -1
    with open(path, 'r') as file:
        for thisLine in file.read().split("\n"):
            if thisLine.__contains__("TrainDataClient"):
                thisClientIdx = int(thisLine.split("TrainDataClient")[1].split(" count")[0])
                thisLabelIdx = int(thisLine.split(" count ")[1].split(": ")[0])
                thisNum = int(thisLine.split(": ")[1])
                if thisNum > maxNum:
                    maxNum = thisNum
                clientLabel2NumMap[str(thisClientIdx) + "-" + str(thisLabelIdx)] = thisNum

    clientNum = thisClientIdx
    labelNum = thisLabelIdx + 1
    labelNames = list(range(labelNum))

    #####################################################################################################
    p2LocalGoal = {}
    for clientIdx in range(1, clientNum + 1):
        p2LocalGoal[clientIdx] = divide100V(
            fileIDIdxClient2RadarMap[fileIDStr + "-" + str(idx) + "-" + str(clientIdx)][0]
        )
    #####################################################################################################
    # p2LocalGoal = {}
    # for clientIdx in range(1, clientNum + 1):
    #     thisClientNList = []
    #     for labelIdx in range(labelNum):
    #         thisClientNList.append(float(clientLabel2NumMap[str(clientIdx) + "-" + str(labelIdx)]) / maxNum)
    #     p2LocalGoal[clientIdx] = thisClientNList
    #####################################################################################################
    return p2LocalGoal, clientNum, labelNum, labelNames


def getFormulation(p2LocalGoal, tNum):
    ###########################################################################
    pNum = len(p2LocalGoal)
    dNum = len(p2LocalGoal[1])
    ###########################################################################
    p2LocalGoalNew = {}
    for pIndex in p2LocalGoal.keys():
        m = {}
        for index in range(len(p2LocalGoal[pIndex])):
            # m[index + 1] = 0.1 * p2LocalGoal[pIndex][index]
            m[index + 1] = p2LocalGoal[pIndex][index]
        p2LocalGoalNew[pIndex] = m
    ###########################################################################
    yita = 0.1
    w = 0.1
    confThreshold = 0.7
    ###########################################################################
    deltaT = 3
    tList = list(range(deltaT, tNum + deltaT, deltaT))
    ###########################################################################
    return [pNum, dNum, tNum, p2LocalGoalNew, yita, w, confThreshold]


def initializeDynMap(pNum, dNum, tNum):
    dynMap = {}
    for pIndex in range(1, pNum + 1):
        dynMap[pIndex] = {}
        for dIndex in range(1, dNum + 1):
            dynMap[pIndex][dIndex] = {}
            for tIndex in range(1, tNum + 1):
                dynMap[pIndex][dIndex][tIndex] = 0
    return dynMap


def findBestTeacherPt(dynMap, pStu, tIndex, pNum, dNum):
    diffSumMax = -1
    pTea = 0
    for pIndex in range(1, pNum + 1):
        diffSum = 0
        for dIndex in range(1, dNum + 1):
            diffSum += abs(dynMap[pIndex][dIndex][tIndex] - dynMap[pStu][dIndex][tIndex])
        if diffSum > diffSumMax:
            diffSumMax = diffSum
            pTea = pIndex
    return pTea


# def runDynSys(tNum, pNum, dNum, a1, a2, w1, w2, p2LocalGoal, wayIndex):
#     dynMap = initializeDynMap(pNum, dNum, tNum)
#     t2pSquareSumMap = {}
#     for tIndex in range(2, tNum + 1):
#         p2SquareSumMap = {}
#         for pIndex in range(1, pNum + 1):
#             squareSum = 0
#             pTea = findBestTeacherPt(dynMap, pIndex, pNum, dNum, tIndex - 1)
#             for dIndex in range(1, dNum + 1):
#                 if wayIndex == 1:
#                     ############################################################################
#                     # FedMD
#                     s = 0
#                     for pIndex2 in range(1, pNum + 1):
#                         s += dynMap[pIndex2][dIndex][tIndex - 1]
#                     s = s / pNum
#                     fedMDGoal = s
#                     distillationGoal = fedMDGoal
#                     thisGoal = distillationGoal
#                     # if p2LocalGoal[pIndex][dIndex] >= a1:
#                     #     thisGoal = w1 * p2LocalGoal[pIndex][dIndex] + (1 - w1) * distillationGoal
#                     # else:
#                     #     thisGoal = distillationGoal
#                     ############################################################################
#                 else:
#                     ############################################################################
#                     # F
#                     distillationGoal = dynMap[pTea][dIndex][tIndex - 1]
#
#                     if dynMap[pTea][dIndex][tIndex - 1] >= a2:
#                         thisGoal = w1 * p2LocalGoal[pIndex][dIndex] + (1 - w1) * distillationGoal
#                     elif dynMap[pTea][dIndex][tIndex - 1] < a2:
#                         thisGoal = p2LocalGoal[pIndex][dIndex]
#                     ############################################################################
#                 ###################################################
#                 dynMap[pIndex][dIndex][tIndex] = w2 * dynMap[pIndex][dIndex][tIndex - 1] + (1 - w2) * thisGoal
#                 # if thisGoal is None:
#                 #     dynMap[pIndex][dIndex][tIndex] = dynMap[pIndex][dIndex][tIndex - 1]
#                 # else:
#                 #     dynMap[pIndex][dIndex][tIndex] = w2 * dynMap[pIndex][dIndex][tIndex - 1] + (1 - w2) * thisGoal
#                 ###################################################
#                 squareSum += dynMap[pIndex][dIndex][tIndex] ** 2
#                 ###################################################
#             p2SquareSumMap[pIndex] = squareSum
#         t2pSquareSumMap[tIndex] = p2SquareSumMap
#
#     return t2pSquareSumMap, dynMap


def runDynSys(pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, wayIndex):
    dynMap = initializeDynMap(pNum, dNum, tNum)
    t2pSquareSumMap = {}
    for tIndex in range(2, tNum + 1):
        p2SquareSumMap = {}
        for pStu in range(1, pNum + 1):
            squareSum = 0
            pTea = findBestTeacherPt(dynMap, pStu, tIndex - 1, pNum, dNum)
            for dIndex in range(1, dNum + 1):
                thisGoal = getThisGoal(pNum, p2LocalGoal, pStu, dIndex, tIndex, pTea, dynMap, confThreshold, w,
                                       wayIndex)
                dynMap[pStu][dIndex][tIndex] = yita * dynMap[pStu][dIndex][tIndex - 1] + (1 - yita) * thisGoal
                ###################################################
                squareSum += dynMap[pStu][dIndex][tIndex] ** 2
                ###################################################
            p2SquareSumMap[pStu] = squareSum
        t2pSquareSumMap[tIndex] = p2SquareSumMap

    return dynMap, t2pSquareSumMap


def getThisGoal(pNum, p2LocalGoal, pStu, dIndex, tIndex, pTea, dynMap, confThreshold, w, wayIndex):
    if wayIndex == 1:
        # FedMD
        s = 0
        for pIndex in range(1, pNum + 1):
            s += dynMap[pIndex][dIndex][tIndex - 1]
        s = s / pNum
        thisGoal = w * p2LocalGoal[pStu][dIndex] + (1 - w) * s
    else:
        # Ours
        distillationGoal = dynMap[pTea][dIndex][tIndex - 1]
        W = getW(distillationGoal, confThreshold, w)
        thisGoal = W * p2LocalGoal[pStu][dIndex] + (1 - W) * distillationGoal
    return thisGoal


def getW(distillationGoal, confThreshold, w):
    if distillationGoal >= confThreshold:
        W = w
    else:
        W = 1
    return W


def getP2List(pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, wayIndex):
    dynMap, t2pSquareSumMap = runDynSys(pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, wayIndex)

    p2List = {}
    for pIndex in range(1, pNum + 1):
        p2List[pIndex] = []
        for tIndex in range(2, tNum + 1):
            p2List[pIndex].append(t2pSquareSumMap[tIndex][pIndex])
    return dynMap, p2List


# def getDynSimulation(eachClientIterRadarLisMap):
#     [pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, tList] = getFormulation(p2LocalGoal)
#
#     dynMap1, p2List1 = getP2List(pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, wayIndex=1)
#     dynMap2, p2List2 = getP2List(pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, wayIndex=2)
#
#     mapPT2ConfList = getAndPltMapPT2ConfList(eachClientIterRadarLisMap, pNum, dNum, tList, dynMap1, dynMap2)
#     return mapPT2ConfList


def getDynSimulation(p2LocalGoal, tNum):
    [pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold] = getFormulation(p2LocalGoal, tNum)

    dynMap1, p2List1 = getP2List(pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, wayIndex=1)
    dynMap2, p2List2 = getP2List(pNum, dNum, tNum, p2LocalGoal, yita, w, confThreshold, wayIndex=2)
    return dynMap1, p2List1, dynMap2, p2List2


def getAndPltMapPT2ConfList(eachClientIterRadarLisMap, pNum, dNum, tList, dynMap1, dynMap2):
    mapPT2ConfList = {}
    for pIndex in range(1, pNum + 1):
        for tPickIndex in range(len(tList)):
            plt.subplot(len(tList), pNum, tPickIndex * pNum + pIndex)
            tIndex = tList[tPickIndex]

            confListThisPtThisIter1 = []
            for dIndex in range(1, dNum + 1):
                confListThisPtThisIter1.append(dynMap1[pIndex][dIndex][tIndex])

            confListThisPtThisIter2 = []
            for dIndex in range(1, dNum + 1):
                confListThisPtThisIter2.append(dynMap2[pIndex][dIndex][tIndex])

            mapPT2ConfList[str(pIndex) + "-" + str(tPickIndex + 1)] = \
                {"FedMD": confListThisPtThisIter1, "F": confListThisPtThisIter2}

            ###########################################################################
            # plt.plot(confListThisPtThisIter1,
            #          color='k', marker='d', linestyle='-', markersize=4,
            #          alpha=0.9, linewidth=3, label="FedMD"
            #          )
            ###########################################################################
            plt.plot(confListThisPtThisIter2,
                     color='r', marker='d', linestyle='-', markersize=4,
                     alpha=0.9, linewidth=2, label="F60"
                     )
            ###########################################################################
            plt.plot(eachClientIterRadarLisMap[str(tPickIndex + 2) + "-" + str(pIndex)],
                     color='b', marker='d', linestyle='-', markersize=4,
                     alpha=0.9, linewidth=2, label="ExpResult"
                     )
            ###########################################################################
            plt.title("Iter" + str(tPickIndex) + " Client" + str(pIndex))
            plt.ylabel("Conf")
            plt.legend()
            plt.grid()
            plt.ylim(0, 1)
    return mapPT2ConfList


def getFileID2NameMap(directoryPath):
    fileID2NameMap = {}
    for root, dirs, files in os.walk(directoryPath):
        if not root.__contains__("Dust"):
            thisFileName = root.split("/")[-1]
            if root.split("/")[-1].__contains__("_"):
                fileID2NameMap[thisFileName.split("_")[1]] = thisFileName
    return fileID2NameMap


def getRowAndCol(N):
    minDiff = 10000
    nRow = 0
    for i in range(1, N + 1):
        if N % i == 0:
            if abs(int(N / i) - i) < minDiff:
                minDiff = abs(int(N / i) - i)
                nRow = i
    return [nRow, int(N / nRow)]


def pltHist(fileID2RMap, fileIDList, fileID, clientNum, labelNum, indexClientLabel2NumMap, thisTitle, rN, cN,
            isLegend=False):
    plt.subplot(rN, cN, fileIDList.index(fileID) + 1)
    labelDistribution = getLabelDis(labelNum, indexClientLabel2NumMap)
    labelList = list(range(len(labelDistribution)))

    plt.hist(labelDistribution, stacked=True, bins=np.arange(-0.5, clientNum + 1.5, 1), label=labelList, rwidth=0.5)
    plt.xticks(np.arange(1, clientNum + 1), ["Client %d" % c_id for c_id in range(1, clientNum + 1)], rotation=60)
    plt.xlim(0, clientNum + 1)
    # plt.xlabel("Client ID")
    plt.ylabel("Number of samples")
    # plt.title(thisTitle + "-" + fileID2RMap[fileID]["thisTitle"])
    plt.title(dealWithTitle(fileID2RMap[fileID]["thisTitle"]))
    if isLegend:
        plt.legend()
    plt.show()


def getTable3(outputFile2, resultName2IdxMap, dataNameList, nonIIDList, fw2Plt, tableMapAccMaf1Mif1,
              nonIIDParameterMap):
    boldKeySetAcc, boldKeySetMaf1, boldKeySetMif1 = getBoldSet(dataNameList, nonIIDList, tableMapAccMaf1Mif1,
                                                               nonIIDParameterMap)

    s = []
    getTable(s, "acc", resultName2IdxMap, dataNameList, nonIIDList, fw2Plt, tableMapAccMaf1Mif1, nonIIDParameterMap,
             boldKeySetAcc)
    getTable(s, "maf1", resultName2IdxMap, dataNameList, nonIIDList, fw2Plt, tableMapAccMaf1Mif1, nonIIDParameterMap,
             boldKeySetMaf1)
    getTable(s, "mif1", resultName2IdxMap, dataNameList, nonIIDList, fw2Plt, tableMapAccMaf1Mif1, nonIIDParameterMap,
             boldKeySetMif1)

    with open(outputFile2, 'w') as file:
        for v in s:
            file.write(v + '\n')


def getImageSizeStr(v):
    b = str(v[3]).split("[")[1].split("]")[0].split(", ");
    a = b[0] + "$" + "\\" + "times$" + b[1] + "$" + "\\" + "times$" + b[2];
    return a


def getDataBasicSta(fileIDList, fileID2RMap, fileID2TrainTestDataNumSizeMap, dataName2SourceMap):
    s = []
    s.append('\\' + 'begin{adjustbox}{width=1.1' + '\\' + 'textwidth}')
    s.append('\\' + 'begin{tabular}{lcccccc}')
    s.append('\\' + 'toprule')
    s.append('\\' + 'cmidrule(r){1-7}')
    s.append('Data Type & Data Set & Train Num & Test Num & Image Size & Class Num & Data Source ' + '\\' + '\\')
    s.append('\\' + 'cmidrule(r){1-7}')

    dataNameSet = set()

    for fileID in fileIDList:
        v = fileID2TrainTestDataNumSizeMap[fileID]
        if v[0] in dataNameSet:
            continue
        if v[0] == "M":
            s.append(
                '\\' + 'multirow{2}{1cm}{' + '\\' + 'centering Basic Data} & ' + fileID2RMap[fileID]['dataNameMap'][
                    v[0]] +
                ' & ' + str(v[1]) + ' & ' + str(v[2]) + ' & ' + getImageSizeStr(v) + ' & ' + str(
                    v[4]) + ' & ' + dataName2SourceMap[v[0]] + ' \\' + '\\')
        elif v[0] == "B":
            s.append('\\' + 'cmidrule(r){1-7}')
            s.append(
                '\\' + 'multirow{3}{1cm}{' + '\\' + 'centering Medical Data} & ' + fileID2RMap[fileID]['dataNameMap'][
                    v[0]] +
                ' & ' + str(v[1]) + ' & ' + str(v[2]) + ' & ' + getImageSizeStr(v) + ' & ' + str(
                    v[4]) + ' & ' + dataName2SourceMap[v[0]] + ' \\' + '\\')
        else:
            s.append('\\' + 'cmidrule(r){2-7}')
            s.append('& ' + fileID2RMap[fileID]['dataNameMap'][v[0]] +
                     ' & ' + str(v[1]) + ' & ' + str(v[2]) + ' & ' + getImageSizeStr(v) + ' & ' + str(
                v[4]) + ' & ' + dataName2SourceMap[v[0]] + ' \\' + '\\')
        dataNameSet.add(v[0])

    s.append('\\' + 'bottomrule')
    s.append('\\' + 'hline')
    s.append('\\' + 'end{tabular}')
    s.append('\\' + 'end{adjustbox}')
    s.append('   ')

    return s


def genDataStaExp(fileIDList, fileID2DsMap, fileID2RMap, fileID2TrainTestDataNumSizeMap, dataName2SourceMap,
                  outputFile):
    sListAll = getDataBasicSta(fileIDList, fileID2RMap, fileID2TrainTestDataNumSizeMap, dataName2SourceMap)
    for fileID in fileIDList:
        sList = genLatexForOneExp(
            fileID2RMap[fileID]['thisTitle'],
            fileID2RMap[fileID]['clientNum'], fileID2DsMap[fileID]['labelNum'],
            fileID2DsMap[fileID]['indexClientLabel2NumMap'],
            fileID2DsMap[fileID]['testDataLabel2NumMap'],
            fileID2DsMap[fileID]['pubDataLabel2NumMap']
        )
        sListAll += sList

    with open(outputFile, 'w') as file:
        for v in sListAll:
            file.write(v + '\n')


def getEachClient2DataNumMap(fileID, fileID2RMap, fileID2DsMap):
    eachClient2DataNumMap = {}
    for clientIdx in range(1, fileID2RMap[fileID]['clientNum'] + 1):
        eachClient2DataNumMap[clientIdx] = 0
        for labelIdx in range(fileID2DsMap[fileID]['labelNum']):
            eachClient2DataNumMap[clientIdx] += fileID2DsMap[fileID]['indexClientLabel2NumMap'][
                str(clientIdx) + "-" + str(labelIdx)]
    print("eachClient2DataNumMap =", eachClient2DataNumMap)
    return eachClient2DataNumMap


def roundListModify(v, N):
    vNew = []
    for x in v:
        vNew.append(round(x, N))

    if len(vNew) == 1:
        return vNew[0]
    return vNew


def pltHistAll(fileIDList, fileID2RMap, fileID2DsMap, rN, cN, isLegend):
    for fileID in fileIDList:
        pltHist(
            fileID2RMap, fileIDList, fileID,
            fileID2RMap[fileID]['clientNum'], fileID2DsMap[fileID]['labelNum'],
            fileID2DsMap[fileID]['indexClientLabel2NumMap'], fileID, rN, cN, isLegend=isLegend
        )


def inverseV(v):
    vNew = []
    for i in range(len(v)):
        vNew.append(v[len(v) - 1 - i])
    return vNew

# def getAccExp(fileIDList, frameworkList, dataNameList, nonIIDList, outputFile):
#     tableAccInforMap = getTableAccInforMap(fileIDList)
#
#     sList = [
#         "\\" + "begin{tabular}{lcccccccccccc}",
#         "\\" + "toprule",
#         "\\" + "cmidrule(r){1-13}",
#         "\\" + "cmidrule(r){1-13}",
#         "\\" + "multirow{2}{1cm}{" + "\\" + "centering " + "\\" + "textbf{Method}}&" + "\\" +
#         "multicolumn{2}{c}{" + "\\" + "textbf{MNIST}} &" + "\\" +
#         "multicolumn{2}{c}{" + "\\" + "textbf{CIFAR-10}} &" + "\\" +
#         "multicolumn{2}{c}{" + "\\" + "textbf{SATE Data}} &" + "\\" +
#         "multicolumn{2}{c}{" + "\\" + "textbf{LC Data}} &" + "\\" +
#         "multicolumn{2}{c}{" + "\\" + "textbf{BTumor Data}} &" + "\\" +
#         "multicolumn{2}{c}{" + "\\" + "textbf{Knee Data}} " + "\\\\",
#         "\\" + "cmidrule(r){2-3}" + "\\" + "cmidrule(r){4-5}" + "\\" + "cmidrule(r){6-7}" + "\\" + "cmidrule(r){8-9}" + "\\" + "cmidrule(r){10-11}" + "\\" + "cmidrule(r){12-13}",
#         "& Normal & Dirichlet & Normal & Dirichlet & Normal & Dirichlet & Normal & Dirichlet & Normal & Dirichlet & Normal & Dirichlet \\" + "\\",
#         "\\" + "cmidrule(r){1-13}"
#     ]
#
#     for fwName in frameworkList:
#         if fwName == "Ours":
#             s = "\\" + "textbf{" + fwName + "}"
#         else:
#             s = fwName
#         s += " & "
#         for d in dataNameList:
#             for n in nonIIDList:
#                 thisKey = d + "-" + n + "-" + fwName
#                 if thisKey in tableAccInforMap.keys():
#                     ############################################################
#                     # thisAcc = round(tableAccInforMap[thisKey][0], 2)
#                     thisAcc = roundListModify(tableAccInforMap[thisKey], 2)
#                     ############################################################
#                 else:
#                     thisAcc = "X"
#                 if fwName == "Ours":
#                     s += "\\" + "textbf{" + str(thisAcc) + "}" + " & "
#                 else:
#                     s += str(thisAcc) + " & "
#         sList.append(s[:-3] + " \\\\")
#
#     sList.append("\\" + "cmidrule(r){1-13}")
#     sList.append("\\" + "end{tabular}")
#
#     with open(outputFile, 'w') as file:
#         for v in sList:
#             file.write(v + '\n')
