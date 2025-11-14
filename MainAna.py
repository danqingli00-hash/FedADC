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
from FedXXX.ToolsAna import pltAccAll, genDataStaExp, pltHistAll, pltAccAverAll, pltRadar, \
    pltClientStuTea, getTable3, getRobustTestOutput, pltThresholdTest, getPaperResult, estimateEndTime, \
    getExpFileIDJustBenchmarks, getExpFileIDJustOurs, getExpFileIDAll, pltThresholdTestNew, \
    getExpFileIDJustOursAndFedMD, basicInfor, getExpFileIDJustOursAndFedMDForLC03, getPltInfor, getPltExpInput, \
    getRowAndCol, pltAccFcn, getTitle2IdxMap, getTeacherFreTotalMap, getEachClient2DataNumMap, getValueFromList, \
    pltBetaCompare, getGenPltInput, pltTwoLinesIDGenPubCompare, getDynSimulation, getOneExpResult, \
    getEachClient2ConfListMap, getP2LocalGoalFromOriData, divide100V, getOneClientOneFwADTrail, pltTrail, getVSumList

######################################################################################################################
averageLastRatio, dataName2SourceMap, outputFile1, outputFile2, outputFile3 = basicInfor()
######################################################################################################################
# fw2Plt = [
#     ["Ours-0.65", "red", 3, "-", 0.6],
#     ["Ours-0.70", "yellow", 3, "-", 0.6],
#     ["Ours-0.75", "blue", 3, "-", 0.6],
#     ["Ours-0.80", "green", 3, "-", 0.6],
#     ["Ours-0.85", "purple", 3, "-", 0.6],
#     ["Ours-0.90", "tomato", 3, "-", 0.6],
#     ["FedAPEN", "black", 1, "-", 1.0],  # "olive"
#     ["FedTGP", "black", 1, "-", 1.0],  # "olive"
#     ["Cronus", "black", 1, "-", 1.0],  # "olive"
#     ["FedDF", "black", 1, "-", 1.0],  # "magenta"
#     ["FedProto", "black", 1, "-", 1.0],  # "cyan"
#     ["FedGEMS", "black", 1, "-", 1.0],  # "violet"
#     ["FedMD", "black", 2, "--", 1.0],  # "black"
#     ["FedProx", "black", 1, "-", 1.0],  # "tomato"
#     ["FedAvg", "black", 1, "-", 1.0],  # "green"
# ]

fw2Plt = [
    ["Ours-0.65", "red", 3, "-", 0.6],
    ["Ours-0.70", "yellow", 3, "-", 0.6],
    ["Ours-0.75", "blue", 3, "-", 0.6],
    ["Ours-0.80", "green", 3, "-", 0.6],
    ["Ours-0.85", "purple", 3, "-", 0.6],
    ["Ours-0.90", "black", 3, "-", 0.6],
    ["FedAPEN", "yellow", 1, "-", 1.0],  # "olive"
    ["FedTGP", "magenta", 1, "-", 1.0],  # "olive"
    ["Cronus", "cyan", 1, "-", 1.0],  # "olive"
    ["FedDF", "green", 1, "-", 1.0],  # "magenta"
    ["FedProto", "blue", 1, "-", 1.0],  # "cyan"
    # ["FedGEMS", "yellow", 1, "-", 1.0],  # "violet"
    ["FedMD", "olive", 1, "-", 1.0],  # "black"
    ["FedProx", "tomato", 1, "-", 1.0],  # "tomato"
    ["FedAvg", "red", 1, "-", 1.0],  # "green"
]

######################################################################################################################
fileIDListInput = [
    # ['20250715193452_041870', '-'],  # L_beta0.3_0.90, Pub, GEN
    # ['20250715234253_085819', '-'],  # L_beta0.3_0.90_(2), Pub, GEN

    ['20250616190753_050361', '-'],  # M_0.1 (15 fw)
    # ['20250624095904_078609', '-'],  # M_0.1_65-70-75-80-85-90 (added)

    # ['20250712225616_028181', '-'],  # M_0.1, Gen, saved, give up
    # ['20250713093712_063903', '-'],  # M_0.1, Gen, saved, give up

    ['20250619111335_018997', '-'],  # M_0.3 (15 fw)
    ['20250621151912_083574', '-'],  # M_0.3_65-70-75-80-85-90 (added)

    # ['20250716104534_037397', '-'],  # M_beta0.3_Ours0.85, GEN, give up
    ['20250714220558_043397', '-'],  # M_beta0.3_0.85, Gen, saved
    ['20250715101843_084484', '-'],  # M_beta0.3_0.85, Pub, saved

    ['20250618141254_025423', '-'],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
    ['20250624140511_099715', '-'],  # S_0.1_65-70-75-80-85-90 (added)
    # ['20250703133844_053730'], rerun S_0.1_Ours_0.85, replaced
    # ['20250704101606_077538'], rerun S_0.1_Ours_0.70, replaced
    # ['20250704102638_094304'], rerun S_0.1_Ours_0.80, replaced
    # ['20250704165238_056083'], rerun S_0.1_Ours_0.65-0.75-0.90, replaced
    # ['20250706132036_007054'], rerun S_0.1_Ours_0.65-0.80-0.90, replaced

    ['20250619111551_013657', '-'],  # S_0.3 (15 fw)
    ['20250624233644_021352', '-'],  # S_0.3_65-70-75-80-85-90 (added)
    # ['20250630161204_093662'], rerun S_0.3_Prox-Avg thisLr: 0.0001 thisBatch: 128 added
    # ['20250630194747_053931'], rerun S_0.3_FedDF thisLr: 0.0001 thisBatch: 16 added
    # ['20250702162735_052470'], rerun S_0.3_Cronus, added
    # ['20250703172023_049640'], rerun S_0.3_Ours70-85, replaced
    # ['20250704102124_095022'], rerun S_0.3_Ours_0.85, replaced

    ['20250618142044_000804', '-'],  # B_0.1 (15 fw)
    ['20250623211522_087167', '-'],  # B_0.1_65-70-75-80-85-90 (added)
    # ['20250630170147_074618'], rerun B_0.1_APEN, replaced
    # ['20250701100758_075500'], rerun B_0.1_Proto, replaced
    # ['20250702231502_007675'], rerun B_0.1_Cronus, added
    # ['20250703164604_011555'], rerun B_0.1_Ours_0.90, replaced

    ['20250619160516_027627', ''],  # B_0.3 (15 fw)
    ['20250621081442_055955', '-'],  # B_0.3_65-70-75-80-85-90 (added)
    # ['20250630170406_056207'], rerun B_0.3_APEN, replaced
    # ['20250703103736_047369'], rerun B_0.3_Cronus, added
    # ['20250703165008_016728'], rerun B_0.3_Ours_0.65, replaced

    ['20250712131126_091915', ''],  # B_0.5_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
    # ['20250718225332_005943', ''],  # B_0.5_Ours85-70 added
    # ['20250718225702_045818', ''],  # B_0.5_Ours70-85 added
    # ['20250716184256_060047', ''],  # B_0.5_Ours85-80-75-70-65-60-85+80 added
    # ['20250715095753_041050', ''],  # rerun_B_beta0.5_0.9_Ours, replaced
    # ['20250711172417_063693']  # B_0.5_Ours, saved, added into 20250712131126_091915
    # ['20250712020426_080910']  # B_0.5_APEN, saved, added into 20250712131126_091915
    # ['20250711174806_088308']  # B_0.5_TGP-DF, saved, added into 20250712131126_091915
    # ['20250712004035_059117']  # B_0.5_Proto-MD-Prox-Avg, saved, added into 20250712131126_091915

    ['20250711215000_096563', ''],  # B_0.7_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
    # ['20250716184839_070831', ''],  # B_0.7_Ours85-80-75-70-65-60-85-80 added
    # ['20250714225358_008075', ''],  # rerun_B_beta0.7_0.9_Ours, saved, added into 20250711215000_096563
    # ['20250711172917_090451']  # B_0.7_Ours, saved, added into 20250711215000_096563
    # ['20250712080113_034617']  # B_0.7_APEN, saved, added into 20250711215000_096563
    # ['20250712200237_032481']  # B_0.7_Cronus, saved, added into 20250711215000_096563
    # ['20250713092256_073696']  # B_0.7_Proto-MD-Prox-Avg, saved, added into 20250711215000_096563

    ['20250712003058_080632', ''],  # B_0.9_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
    # ['20250719175122_068859', ''],  # B_0.9_Ours70-65, running
    # ['20250719095725_039273', ''],  # B_0.9_Ours65-70, running
    # ['20250716185039_035302', ''],  # B_0.9_Ours85-80-75-70-65-60, added
    # ['20250711173208_007512']  # B_0.9_Ours, saved, added into 20250712003058_080632
    # ['20250712080708_048660']  # B_0.9_APEN, saved, added into 20250712003058_080632
    # ['20250712201205_046099']  # B_0.9_Cronus, saved, added into 20250712003058_080632
    # ['20250713092953_075459']  # B_0.9_Proto-MD-Prox-Avg, saved, added into 20250712003058_080632

    ['20250618143322_034012', ''],  # K_0.1 (15 fw)
    ['20250623212407_065360', '-'],  # K_0.1_65-70-75-80-85-90 (added)
    # ['20250630231158_039371'], rerun K_0.1_FedDF thisLr: 0.0001 thisBatch: 16 added
    # ['20250702231053_048703'], rerun K_0.1_Cronus, added
    # ['20250703171355_070831'], rerun K_0.1_Ours70-85-90, replaced
    # ['20250704104633_068260'], rerun K_0.1_Ours_0.70, replaced
    # ['20250704221328_073501'], rerun K_0.1_Ours_0.80, replaced

    ['20250619111744_055767', ''],  # K_0.3 (15 fw)
    ['20250621075843_084608', '-'],  # K_0.3_65-70-75-80-85-90 (added)
    # ['20250702165251_096883'], rerun K_0.3_Cronus, added
    # ['20250704134833_021791'], rerun K_0.3_Ours_0.85, replaced

    ['20250713234603_083070', ''],  # K_0.5_Ours, saved
    # ['20250716230931_033515', ''],  # K_0.5_Ours85-80-75-70-65-60, 85+80+75+70+65+60added
    # ['20250714085152_032595', '-'],  # K_0.5_APEN-TGP-DF, saved, added into 20250713234603_083070
    # ['20250714000439_065764', '-'],  # K_0.5_Cronus-Proto-MD-Prox-Avg, saved, added into 20250713234603_083070

    ['20250713235053_091597', ''],  # K_0.7_Ours, saved
    # ['20250717212821_062638', ''],  # K_0.7_Ours70-65-60, added
    # ['20250714085718_063387', '-'],  # K_0.7_APEN-TGP-DF, saved, added into 20250713235053_091597
    # ['20250714001148_063149', '-'],  # K_0.7_Cronus-Proto-MD-Prox-Avg, saved, added into 20250713235053_091597
    # ['20250715230012_041952']  # K_beta0.7_0.9_Ours, replaced
    # ['20250716102636_008527']  # K_beta0.7_0.75_Ours, added
    # ['20250716103723_075317']  # K_beta0.7_0.80_Ours, added
    # ['20250716182818_083702']  # K_beta0.7_85_Ours, added
    # ['20250715201604_088969']  # K_beta0.7_MD, replaced
    # ['20250715202154_064096']  # K_beta0.7_TGP, replaced

    ['20250713235249_007780', ''],  # K_0.9_Ours, saved
    # ['20250718140454_018884', ''],  # K_0.9_Ours90, added
    # ['20250718140907_031659', ''],  # K_0.9_Ours85, added

    # ['20250717230205_038057', ''],  # K_0.9_Ours60-65-70-85, added
    # ['20250716102940_087879']  # K_beta0.9_0.75_Ours, added
    # ['20250716103500_068898']  # K_beta0.9_0.80_Ours, added
    # ['20250714094827_088173', '-'],  # K_0.9_APEN-TGP-DF, saved, added into 20250713235249_007780
    # ['20250714170355_024562', '-'],  # K_0.9_Cronus-Proto-MD-Prox-Avg, saved, added into 20250713235249_007780
    # ['20250715230120_099867']  # K_beta0.9_0.9_Ours, replaced

    ['20250620220350_018565', ''],  # L_0.1
    # L_0.1_50data, (0Ours, 1FedAPEN, 2FedTGP, 3FedDF, 6FedProto, 7FedMD, 8FedProx, 9FedAvg)
    # 65: 0(added),    70: 10(added),    75: 11(added),    80: 12(added),    85: 13(added),    90: 14(added)
    # (20250620220350_018565, 0Ours added 1FedAPEN added 2TGP added) + (3FedDF added) + (20250626094240_078275, 6Proto added) + (20250628124029_089298, MD added) + (20250626110930_073187, Prox-Avg added)
    ['20250625231904_057633', '-'],  # L_0.1_65(added)-70-75(added)
    # 65: 0(added),    70: 1(added),    75: 2(added),    80: 3(added),    85: 4(added),    90: 5(added)
    # '20250626150128_071769',  # L_0.1_85(added)-90(added)
    # ['20250703094547_071610'], rerun L_0.1_Cronus, added

    ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 1FedAPEN, 3FedDF, 6FedProto, 7FedMD, 8FedProx, 9FedAvg)
    ['20250716004043_061963', '-'],  # L_beta0.3_0.90, Generated
    ['20250715234253_085819', '-'],  # L_beta0.3_0.90, Generated
    # 65: 0(added),    70: 10(added),    75: 11(added),    80: 12(added),    85: 13(added),    90: 14(added)
    # (20250622000033_074801, Ours-APEN added) + (20250629212840_044334, TGP added) + (3FedDF added) + (20250626094433_009690, 6Proto added, 7MD added) + (20250626112546_013381, Prox-Avg added)
    ['20250625224910_012705', '-'],  # L_0.3_65-70
    # 65: 0(added),    70: 1(added),    75: 2(added),    80: 3(added),    85: 4(added),    90: 5(added)
    # ['20250629153336_069793', ''],  # L_0.3_75 (added)
    # '20250626150738_093495',  # L_0.3_85(added)
    # '20250630150107_008277',  # L_0.3_90 (added)
    # ['20250703094833_045571'], rerun L_0.3_Cronus, added
    # ['20250701101452_084228'], rerun L_0.3_Proto, replaced
]
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
fw2Plt = [
    ["Ours-0.65", "red", 3, "-", 0.6],
    ["Ours-0.70", "yellow", 3, "-", 0.6],
    ["Ours-0.75", "blue", 3, "-", 0.6],
    ["Ours-0.80", "green", 3, "-", 0.6],
    ["Ours-0.85", "purple", 3, "-", 0.6],
    ["Ours-0.90", "black", 3, "-", 0.6],
    ["FedAPEN", "lightblue", 1, "-", 1.0],  # "olive"
    ["FedTGP", "gray", 1, "-", 1.0],  # "olive"
    ["Cronus", "dimgray", 1, "-", 1.0],  # "olive"
    ["FedDF", "lightseagreen", 1, "-", 1.0],  # "magenta"
    ["FedProto", "turquoise", 1, "-", 1.0],  # "cyan"
    # ["FedGEMS", "yellow", 1, "-", 1.0],  # "violet"
    ["FedMD", "olive", 1, "-", 1.0],  # "black"
    ["FedProx", "teal", 1, "-", 1.0],  # "tomato"
    ["FedAvg", "lightskyblue", 1, "-", 1.0],  # "green"
]

fw2Plt = [
    ["Ours-0.65", "red", 3, "-", 0.6],
    ["Ours-0.70", "yellow", 3, "-", 0.6],
    ["Ours-0.75", "blue", 3, "-", 0.6],
    ["Ours-0.80", "green", 3, "-", 0.6],
    ["Ours-0.85", "purple", 3, "-", 0.6],
    ["Ours-0.90", "black", 3, "-", 0.6],
    # ["FedAPEN", "yellow", 1, "-", 1.0],  # "olive"
    # ["FedTGP", "magenta", 1, "-", 1.0],  # "olive"
    # ["Cronus", "cyan", 1, "-", 1.0],  # "olive"
    # ["FedDF", "green", 1, "-", 1.0],  # "magenta"
    # ["FedProto", "blue", 1, "-", 1.0],  # "cyan"
    # ["FedGEMS", "yellow", 1, "-", 1.0],  # "violet"
    # ["FedMD", "olive", 1, "-", 1.0],  # "black"
    # ["FedProx", "tomato", 1, "-", 1.0],  # "tomato"
    # ["FedAvg", "red", 1, "-", 1.0],  # "green"
]

fw2Plt = [
    # ["Ours-0.65", "red", 3, "-", 0.6],
    ["Ours-0.70", "yellow", 3, "-", 0.6],
    # ["Ours-0.75", "blue", 3, "-", 0.6],
    # ["Ours-0.80", "green", 3, "-", 0.6],
    # ["Ours-0.85", "purple", 3, "-", 0.6],
    # ["Ours-0.90", "black", 3, "-", 0.6],
    # ["FedAPEN", "yellow", 1, "-", 1.0],  # "olive"
    # ["FedTGP", "magenta", 1, "-", 1.0],  # "olive"
    # ["Cronus", "cyan", 1, "-", 1.0],  # "olive"
    # ["FedDF", "green", 1, "-", 1.0],  # "magenta"
    # ["FedProto", "blue", 1, "-", 1.0],  # "cyan"
    # ["FedGEMS", "yellow", 1, "-", 1.0],  # "violet"
    ["FedMD", "olive", 1, "-", 1.0],  # "black"
    # ["FedProx", "tomato", 1, "-", 1.0],  # "tomato"
    # ["FedAvg", "red", 1, "-", 1.0],  # "green"
]

fileIDListInput = [
    ['20250616190753_050361', ''],  # M_0.1 (15 fw)
    ['20250618141254_025423', ''],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
    ['20250620220350_018565', ''],  # L_0.1
    ['20250618142044_000804', ''],  # B_0.1 (15 fw)
    ['20250618143322_034012', ''],  # K_0.1 (15 fw)

    ['20250619111335_018997', ''],  # M_0.3 (15 fw)
    ['20250619111551_013657', ''],  # S_0.3 (15 fw)
    ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 1FedAPEN, 3FedDF, 6FedProto, 7FedMD, 8FedProx, 9FedAvg)
    ['20250619160516_027627', ''],  # B_0.3 (15 fw)
    ['20250619111744_055767', ''],  # K_0.3 (15 fw)
]

fileIDListInput = [
    ['20250618142044_000804', ''],  # B_0.1 (15 fw)
    ['20250619160516_027627', ''],  # B_0.3 (15 fw)
    ['20250712131126_091915', ''],  # B_0.5_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
    ['20250711215000_096563', ''],  # B_0.7_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
    ['20250712003058_080632', ''],  # B_0.9_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved

    ['20250618143322_034012', ''],  # K_0.1 (15 fw)
    ['20250619111744_055767', ''],  # K_0.3 (15 fw)
    ['20250713234603_083070', ''],  # K_0.5_Ours, saved
    ['20250713235053_091597', ''],  # K_0.7_Ours, saved
    ['20250713235249_007780', ''],  # K_0.9_Ours, saved
]

fileIDListInput = [
    ['20250714220558_043397', ''],  # M_beta0.3_0.85, Gen, saved
    ['20250715101843_084484', ''],  # M_beta0.3_0.85, Pub, saved]
    ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 1FedAPEN, 3FedDF, 6FedProto, 7FedMD, 8FedProx, 9FedAvg)
    ['20250716004043_061963', ''],  # L_beta0.3_0.90, Generated
]

fileIDListInput = [
    ['20250616190753_050361', ''],  # M_0.1 (15 fw)
    ['20250618141254_025423', ''],  # S_0.1 (15 fw) # the tail is fluctuating so the tail should be cut
    ['20250620220350_018565', ''],  # L_0.1
    ['20250618142044_000804', ''],  # B_0.1 (15 fw)
    ['20250618143322_034012', ''],  # K_0.1 (15 fw)

    ['20250619111335_018997', ''],  # M_0.3 (15 fw)
    ['20250619111551_013657', ''],  # S_0.3 (15 fw)
    ['20250622000033_074801', ''],  # L_0.3_50data, (0Ours, 1FedAPEN, 3FedDF, 6FedProto, 7FedMD, 8FedProx, 9FedAvg)
    ['20250619160516_027627', ''],  # B_0.3 (15 fw)
    ['20250619111744_055767', ''],  # K_0.3 (15 fw)

    ['20250712131126_091915', ''],  # B_0.5_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
    ['20250711215000_096563', ''],  # B_0.7_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved
    ['20250712003058_080632', ''],  # B_0.9_Ours-APEN-TGP-DF-Cronus-Proto-MD-Prox-Avg, saved

    ['20250713234603_083070', ''],  # K_0.5_Ours, saved
    ['20250713235053_091597', ''],  # K_0.7_Ours, saved
    ['20250713235249_007780', ''],  # K_0.9_Ours, saved
]
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
# iterStartMap = {"acc": 1, "maf1": 1, "mif1": 1, "radar": 2}
######################################################################################################################
pltIndex = 0  # 0: all, 1: Ours, 2: benchmarks
fw2Plt, fileIDListInput = getPltExpInput(pltIndex)

# Gen, M
fw2Plt, fileIDListInput = getGenPltInput()
######################################################################################################################
(fileIDList, fileID2RMap, fileID2DsMap,
 fileID2Idx2Client2AccListMapMap, fileID2Idx2AverageAccMap, fileID2Idx2AccMap,
 fileID2Idx2Client2Maf1ListMapMap, fileID2Idx2AverageMaf1Map, fileID2Idx2Maf1Map,
 fileID2Idx2Client2Mif1ListMapMap, fileID2Idx2AverageMif1Map, fileID2Idx2Mif1Map,
 fileIDIdxClient2RadarMap, fileID2Iter2RShipMap, fileID2LabelNamesMap, fileID2TrainTestDataNumSizeMap,
 tableMapAccMaf1Mif1, title2IdxMap) = (
    getPaperResult(fileIDListInput, averageLastRatio))
######################################################################################################################
# Plot Result
idxAndIfPlt = [
    ["acc", 1],
    ["maf1", 1],
    ["mif1", 0]
]
isLegend = True
isPltFill = False

key2Title2MaxMinDiffMapMap = pltAccFcn(idxAndIfPlt, fileIDList, fileID2RMap, fileID2DsMap, fileID2Idx2AverageAccMap,
                                       fw2Plt, isLegend, isPltFill)
######################################################################################################################
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(5)

barWidth = 0.3

for dataName in ['btumor', 'knee']:
    vList = []
    for beta in [0.1, 0.3, 0.5, 0.7, 0.9]:
        thisKey = dataName + "-" + str(beta)
        print(thisKey, key2Title2MaxMinDiffMapMap['acc'][thisKey])
        vList.append(key2Title2MaxMinDiffMapMap['acc'][thisKey])
    plt.bar(x + ['btumor', 'knee'].index(dataName) * barWidth, vList, tick_label=['0.1', '0.3', '0.5', '0.7', '0.9'],
            width=barWidth, label=dataName)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.ylabel("Acc Max - Min", fontsize=16)
plt.legend(fontsize=16)
plt.show()
######################################################################################################################
# Plot Pub and Gen
pltTwoLinesIDGenPubCompare(fileID2Idx2AverageAccMap)
######################################################################################################################
fwList = ["Ours", "FedAPEN", "FedTGP", "FedDF", "Cronus", "FedProto", "FedMD", "FedProx", "FedAvg"]
# betaList = ['0.1', '0.3', '0.5', '0.7', '0.9']
betaList = ['0.1', '0.3', '0.5', '0.7']

dataNamePltIdxMap = {'knee': 2, 'btumor': 1}

# dataNameHere = 'knee'  # 'btumor', 'knee'
# dataNameHere = 'btumor'  # 'btumor', 'knee'

perIdx = 0  # 0: Acc, 1: MacroF1, 2: MicroF1
dataNameHere = 'btumor'  # 'btumor', 'knee'
pltBetaCompare(fw2Plt, fwList, betaList, dataNameHere, tableMapAccMaf1Mif1, perIdx, dataNamePltIdxMap)
# dataNameHere = 'knee'  # 'btumor', 'knee'
# pltBetaCompare(fw2Plt, fwList, betaList, dataNameHere, tableMapAccMaf1Mif1, perIdx, dataNamePltIdxMap)
######################################################################################################################
# Result Table
######################################################################################################################
dataNameList = ['mnist', 'sate', 'lc', 'btumor', 'knee']
nonIIDParameterMap = {"Very Uneven": 0.1, "Slight Uneven": 0.3}
resultName2IdxMap = {"acc": 0, "maf1": 1, "mif1": 2}

nonIIDList = ["Very Uneven", "Slight Uneven"]
######################################################################################################################
dataNameList = ['btumor', 'knee']
nonIIDParameterMap = {"Beta1": 0.1, "Beta2": 0.3, "Beta3": 0.5, "Beta4": 0.7, "Beta5": 0.9}
resultName2IdxMap = {"acc": 0, "maf1": 1, "mif1": 2}

nonIIDList = ["Beta1", "Beta2", "Beta3", "Beta4", "Beta5"]
######################################################################################################################
getTable3(outputFile2, resultName2IdxMap, dataNameList, nonIIDList, fw2Plt, tableMapAccMaf1Mif1, nonIIDParameterMap)
######################################################################################################################
# Plot Radar: radar1.pdf, radar2.pdf.
# Setting: pltIndex = 0
print(title2IdxMap)
pltIndex = 0

# titleInput = "knee-0.1"
titleInput = "btumor-0.1"
fileID = fileIDList[title2IdxMap[titleInput]]
print(fileID)

ifShadow = False

cMap = {"Ours65": "r", "Ours70": "b", "Ours75": "b", "Ours80": "cyan", "FedMD": "k"}
alphaMap = {"Ours65": 0.6, "Ours70": 0.6, "Ours75": 0.6, "Ours80": 0.6, "FedMD": 0.6}
nPlt = 8

m = \
    {
        # 1: 'FedAPEN', 2: 'FedTGP', 3: 'FedDF', 4: 'Cronus', 5: 'FedGEMS', 6: 'FedProto',
        7: 'FedMD',
        # 8: 'FedProx', 9: 'FedAvg',
        # 0: 'Ours65',
        10: 'Ours70',
        # 11: 'Ours75',
        # 12: 'Ours80',
        # 13: 'Ours85',
        # 14: 'Ours90'
    }

idx = 10
#####################################################################################################
tNum = 100
p2LocalGoal, clientNum, labelNum, labelNames = getP2LocalGoalFromOriData(fileID, fileIDIdxClient2RadarMap, idx)
dynMap1, p2List1, dynMap2, p2List2 = getDynSimulation(p2LocalGoal, tNum)
#####################################################################################################
iterIdx2ClientFwValuesMap, iterIdx2ClientFwValuesDynMap = pltRadar(
    pltIndex,
    fileID,
    nPlt, cMap, alphaMap,
    fileID2RMap[fileID]["iterNum"], fileID2LabelNamesMap[fileID], fileID2RMap[fileID]["clientNum"],
    m, fileIDIdxClient2RadarMap, ifShadow, dynMap1, dynMap2, tNum
)
#####################################################################################################
# iterIdx2ClientFwValuesMap.keys()
#####################################################################################################
import matplotlib.pyplot as plt
import matplotlib.patches as patches

d1, d2 = 0, 1

fig = plt.figure()

clientInput = 3
########################################################
# ax1 = fig.add_subplot(221)
#
# isReal = True
#
# fwInput = "FedMD"
# v1 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesMap)
# pltTrail(v1, ax1, patches, fwInput, clientInput, isReal)
#
# fwInput = "Ours70"
# v2 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesMap)
# pltTrail(v2, ax1, patches, fwInput, clientInput, isReal)
#
# plt.ylabel("Trail", fontsize=20)
########################################################
ax2 = fig.add_subplot(221)

plt.plot(getVSumList(v1), c='k', linestyle='-', linewidth=4, label='Experiment-FedMD')
plt.plot(getVSumList(v2), c='deepskyblue', linestyle='-', linewidth=4, label='Experiment-Ours')

fwInput = "FedMD"
vDyn1 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesDynMap)
fwInput = "Ours70"
vDyn2 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesDynMap)

plt.plot(getVSumList(vDyn1), c='k', linestyle='--', linewidth=4, label='Dynamics-FedMD')
plt.plot(getVSumList(vDyn2), c='deepskyblue', linestyle='--', linewidth=4, label='Dynamics-Ours')

plt.ylabel("Knowledge Growth", fontsize=20)

plt.legend()

ax3 = fig.add_subplot(223)

vFedMD = fileID2Idx2Client2AccListMapMap[fileID][7][clientInput]
vFedOurs70 = fileID2Idx2Client2AccListMapMap[fileID][10][clientInput]

plt.plot(vFedMD, c='k', linestyle='-', linewidth=4, label='Acc-FedMD')
plt.plot(vFedOurs70, c='teal', linestyle='-', linewidth=4, label='Acc-Ours')

plt.ylabel("Acc", fontsize=20)
plt.xlabel("Client 1", fontsize=20)
plt.legend()

clientInput = 4
########################################################
# ax4 = fig.add_subplot(322)
#
# isReal = True
#
# fwInput = "FedMD"
# v1 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesMap)
# pltTrail(v1, ax4, patches, fwInput, clientInput, isReal)
#
# fwInput = "Ours70"
# v2 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesMap)
# pltTrail(v2, ax4, patches, fwInput, clientInput, isReal)
########################################################

ax5 = fig.add_subplot(222)

plt.plot(getVSumList(v1), c='k', linestyle='-', linewidth=4, label='Experiment-FedMD')
plt.plot(getVSumList(v2), c='deepskyblue', linestyle='-', linewidth=4, label='Experiment-Ours')

fwInput = "FedMD"
vDyn1 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesDynMap)
fwInput = "Ours70"
vDyn2 = getOneClientOneFwADTrail(d1, d2, clientInput, fwInput, iterIdx2ClientFwValuesDynMap)

plt.plot(getVSumList(vDyn1), c='k', linewidth=4, linestyle='--', label='Dynamics-FedMD')
plt.plot(getVSumList(vDyn2), c='deepskyblue', linewidth=4, linestyle='--', label='Dynamics-Ours')

plt.legend()

ax6 = fig.add_subplot(224)

vFedMD = fileID2Idx2Client2AccListMapMap[fileID][7][clientInput]
vFedOurs70 = fileID2Idx2Client2AccListMapMap[fileID][10][clientInput]

plt.plot(vFedMD, c='k', linestyle='-', linewidth=4, label='Acc-FedMD')
plt.plot(vFedOurs70, c='teal', linestyle='-', linewidth=4, label='Acc-Ours')
plt.xlabel("Client 2", fontsize=20)
plt.legend()

plt.show()
#####################################################################################################
# Plot Stu And Tea Relationship: radar_evo1.pdf, radar_evo2.pdf, ...
# Setting: pltIndex = 0

titleInput = "knee-0.1"
fileID = fileIDList[title2IdxMap[titleInput]]
idxInput = 14  # 0, 10, 11, 12, 13, 14

rN, cN = 3, 5
pltClientStuTea(titleInput, fileID2RMap, fileID2Iter2RShipMap, idxInput, fileID, rN, cN, 'lightblue', 'black', 30)
######################################################################################################################
# Hist Plt
# ThresholdRobust.pdf
# Robust plot: RobustPlt.pdf

# dataNameList = ['mnist', 'sate', 'lc', 'btumor', 'knee']
# dataNameList = ['btumor', 'knee']
dataNameList = ['btumor']
# qList = [0.1, 0.3, 0.5, 0.7, 0.9]
qList = [0.1, 0.3, 0.5, 0.7]
pList = ['0.65', '0.70', '0.75', '0.80', '0.85', '0.90']
pltThresholdTestNew(tableMapAccMaf1Mif1, dataNameList, qList, pList)
######################################################################################################################
# ThresholdRobust
# Setting: pltIndex = 1

thresholdValueList = ['0.65', '0.70', '0.75', '0.80', '0.85', '0.90']
dataNameList = ["M", "S", "L", "B", "K"]
robustTestFileIDList = [
    ['20250624095904_078609', '20250624140511_099715', '20250625231904_057633', '20250623211522_087167',
     '20250623212407_065360'],
    # M, S, L, B, K, beta = 0.1
    ['20250621151912_083574', '20250624233644_021352', '20250625224910_012705', '20250621081442_055955',
     '20250621075843_084608']
    # M, S, L, B, K, beta = 0.3
]
getRobustTestOutput(pltIndex, outputFile3, robustTestFileIDList, fileID2RMap, fileID2Idx2AccMap, thresholdValueList)
######################################################################################################################
# Input Data Statistics
genDataStaExp(fileIDList, fileID2DsMap, fileID2RMap, fileID2TrainTestDataNumSizeMap, dataName2SourceMap, outputFile1)
# ######################################################################################################################
# # Setting: pltIndex = 0
# import matplotlib.pyplot as plt
#
# count = 1
# for fileID in fileIDList:
#     for idxInput in [0, 10, 11, 12, 13, 14]:
#         # eachClient2DataNumMap = getEachClient2DataNumMap(fileID, fileID2RMap, fileID2DsMap)
#         teacherFreTotalMap, maxPtList = getTeacherFreTotalMap(fileID, fileID2Iter2RShipMap, idxInput)
#         plt.subplot(len(fileIDList), len([0, 10, 11, 12, 13, 14]), count)
#         plt.plot(maxPtList, label='xx', color='red', marker='H', linestyle='--', linewidth=3, alpha=0.6)
#         count += 1
# ######################################################################################################################
# Plot Hist: data_hist.pdf

rN, cN = 4, 4
isLegend = False
pltHistAll(fileIDList, fileID2RMap, fileID2DsMap, rN, cN, isLegend)
######################################################################################################################
[thisTitle, labelNum, clientNum, expNum, iterNum,
 indexClientLabel2NumMap, testDataLabel2NumMap, pubDataLabel2NumMap,
 centralAcc, eachClient2AccListMapList, eachFramework2AccMap,
 dataNameMap, dataDisNameMap, MapFramework] = (getOneExpResult(fileIDList[0]))

eachClientIterRadarLisMap = getEachClient2ConfListMap(fileIDList[0])

# mapPT2ConfList = getDynSimulation(eachClientIterRadarLisMap)
####################################################################################################################
# clientIdx = 1
#
# valuesList = []
# for i in [2, 4, 6, 8, 10]:
#     print(mapPT2ConfList[str(clientIdx) + "-" + str(i)])
#     valuesList.append([mapPT2ConfList[str(clientIdx) + "-" + str(i)]["FedMD"], mapPT2ConfList[str(clientIdx) + "-" + str(i)]["F"]])
# feature = []
# for i in range(10):
#     feature.append("Label" + str(i + 1))
####################################################################################################################
