def readOBJFiles(sourceFile):
    try:
        with open(sourceFile, "r") as fp:
            return fp.readlines();
    except FileNotFoundError:
        print("\nError：所指定要讀取的 OBJ File 並不存在！\n")
        return None

def readRecordWithoutSpace(originalRecord):
    return originalRecord.replace(" ", "")