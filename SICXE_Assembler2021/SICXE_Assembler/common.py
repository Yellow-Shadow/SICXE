import sic

def getMainFileName(filename):
    i = 2
    mainname = ""
    while True:
        if filename[i] == '.':
            break
        mainname += filename[i]
        i += 1
    return mainname

def hasLabel(line):
    if len(line) == 1:                  # Only the possibility of Opcode
        return False
    else:
        # For the Format3 and For the Format4 (e.g. +JSUB)
        if sic.isInstruction(line[0]) or sic.isInstruction(line[0][1:]):
            return False
        else:
            return True