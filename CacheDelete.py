import shutil
import os

localPath = os.getcwd()

if localPath.__contains__("D:"):
    rootPath = 'D:/FedAD/'
elif localPath.__contains__("autodl-tmp/"):
    rootPath = '/autodl-tmp/FedAD/'

sNewList = [
    rootPath + "FedXXX/__pycache__",
    rootPath + "FedXXX/ExpResAna/__pycache__/",
    rootPath + "FedXXX/TestPy/__pycache__/",
]

for sNew in sNewList:
    if os.path.exists(sNew):
        print("(Existing) ", sNew)
        shutil.rmtree(sNew)
