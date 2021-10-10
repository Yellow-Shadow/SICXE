import os
# os.path.splitext(): 函數將文件名和擴展名分開
# os.path.splitext('/home/ubuntu/python/example.py')
# ('/home/ubuntu/python/example', '.py')

def openFile(FileName):
    expandedFileName = os.path.splitext(FileName)[0] + "_expanded.asm"
    expandedFile = open(expandedFileName, "w")
    return expandedFile