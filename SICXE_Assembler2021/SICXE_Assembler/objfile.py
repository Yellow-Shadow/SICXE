import common

def openFile(filename):
    objfilename = common.getMainFileName(filename)
    objfilename = objfilename + ".obj"
    objfile = open(objfilename, "w")
    return objfile

def writeHeader(file, name, starting, proglen):
    header = "H" + programname(name)
    header += hexstrToWord(hex(starting))[2:]
    header += hexstrToWord(hex(proglen))[2:]
    header += "\n"
    file.write(header)
    
def programname(name):
    n = 6 - len(name)
    for i in range(0, n):
        name = name + ' '
    return name

def writeText(file, starting, tline):
    textrecord = "T" + hexstrToWord(hex(starting))[2:]
    l = hex(int(len(tline)/2))
    l = l[2:]
    
    n = 2 - len(l)
    for i in range(0, n):
        l = '0' + l
    
    l = l.upper()
    textrecord += l
    textrecord += tline
    textrecord += "\n"
    file.write(textrecord)
    
def writeModification(file, modification):
    for addr in modification:
        modificationrecord = "M" + hexstrToWord(hex(addr))[2:] + '05\n'
        file.write(modificationrecord)

def writeEnd(file, address):
    endrecord = "E" + hexstrToWord(hex(address))[2:]
    file.write(endrecord)
    file.close()
    
def hexstrToWord(hexstr):
    hexstr = hexstr.upper()
    hexstr = hexstr[2:]
    n = 8 - len(hexstr)
    for i in range(0, n):
        hexstr = '0' + hexstr    
    return hexstr

    
