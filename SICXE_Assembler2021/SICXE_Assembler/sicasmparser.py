def readfile(srcfile):
    try:
        with open(srcfile, "r") as fp:
            return fp.readlines()
    except:
            return None

""" 
第四行的 readlines() 方法讀取整個檔案的所有行，
並儲存在一個列表(list)變數中，每行為一個元素。
"""
    
def removeCommentLineAndGetTokens(lines):
    tokenslist = []
    for line in lines:
        if line[0] == '.':
            continue
        tokens = line.split()
        tokenslist.append(tokens)
    return tokenslist
    
