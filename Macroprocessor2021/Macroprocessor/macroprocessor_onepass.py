import sys
import expandedFile

def GETLINE():
    global fileLineIndex
    global expandedLineIndex
	
    # Get next line of macro definition from DEFTAB
    # Indicates that Program is expanding Macro, so expandingMacroName isn't empty. 
    if len(expandingMacroName) > 0:
        expandedLineIndex += 1
        
        print(f'DEFTAB[{expandingMacroName}][{expandedLineIndex-1}] = ', end = '') 
        print(f' {DEFTAB[expandingMacroName][expandedLineIndex-1]}')
        # e.g. 
		# DEFTAB[MACROX][0] = "RDBUFF	MACRO	&ADDR"
		# DEFTAB[MACROX][1] = "			LDT		&ADDR"
		# DEFTAB[MACROX][2] = "			MEND		 "
		# DEFTAB[RDBUFF][0] = "			LDT		PARA1"
        return DEFTAB[expandingMacroName][expandedLineIndex-1]
		
    # Read next line from input file    
    else:
        #print(fileLineIndex)
        line = lines[fileLineIndex]
        fileLineIndex += 1
        return line
        
def PROCESSLINE(line):
    global fileLineIndex
    global expandingMacroName
    
    # if Blank Line or Comment Out Line, continue.
    # The .strip() method is used to remove the characters specified 
    # at the beginning and end of a string (default is a space " " or newline "\n")
    if line[0] == '.' or line.strip() == '.' or line.strip() == '':   
        return
    else:
        tokens = line.split()
    
    if len(tokens) >= 2 and tokens[1] == "MACRO":
        DEFINE(line)
	# Determine whether it is a call of macro
	# e.g. CLOOP    RDBUFF      F1,BUFFER,LENGTH, RDBUFF is tokens[1]
	# e.g.          WRBUFF      05,BUFFER,LENGTH, WRBUFF is tokens[0]
    elif tokens[0] in DEFTAB or (len(tokens) >= 2 and tokens[1] in DEFTAB):
        # e.g.          WRBUFF      05,BUFFER,LENGTH,
        # WRBUFF is tokens[0]
        if tokens[0] in DEFTAB:
            label = ""
            macroName = tokens[0]
            if len(tokens) >= 2:
                arguments = tokens[1].split(",")
            else:
                arguments = ""
        # e.g. CLOOP    RDBUFF      F1,BUFFER,LENGTH,
        # RDBUFF is tokens[1]
        else:
            label = tokens[0]            
            macroName = tokens[1]
            if len(tokens) >= 3:
                arguments = tokens[2].split(",")
            else:
                arguments = ""
            
        checkLevel = MMLTAB[macroName]
            
        while checkLevel > 1:
            processLine = GETLINE()

            if processLine[0] == '.' or processLine.strip() == '.' or processLine.strip() == '':
                # The more times you use GETLINE(), the lower variable「checkLevel」 will be and
                # and the more variable「fileLineIndex」 you will have to pay back
                fileLineIndex = fileLineIndex - (MMLTAB[macroName] + 1 - checkLevel)
                return
            else:
                tokens = processLine.split()
            
            innerLayerMacroName = []
            # e.g.
            # DEFTAB[macroName] = ['RDBUFF\tMACRO\t&ADDR\n', '\t\tLDT\t\t&ADDR\n', '\t\tMEND\n']
            # DEFTAB[macroName][0].split('\t') = ['RDBUFF', 'MACRO', '&ADDR\n']
            # DEFTAB[macroName][1].split('\t') = ['', '', 'LDT', '', '&ADDR\n']
            # DEFTAB[macroName][2].split('\t') = ['', '', 'MEND\n']
            for i in range(0, len(DEFTAB[f'{macroName}'])):
                if DEFTAB[f'{macroName}'][i].split('\t')[0] != '':
                    innerLayerMacroName.append(DEFTAB[f'{macroName}'][i].split('\t')[0])
            
            #print(f'innerLayerMacroName = {innerLayerMacroName}')
            
            if tokens[0] not in innerLayerMacroName and (len(tokens) >= 2 and tokens[1] not in innerLayerMacroName):
                # The more times you use GETLINE(), the lower variable「checkLevel」 will be and
                # and the more variable「fileLineIndex」 you will have to pay back
                if tokens[0] in DEFTAB or (len(tokens) >= 2 and tokens[1] in DEFTAB):
                    fileLineIndex = fileLineIndex - (MMLTAB[macroName] + 0 - checkLevel)
                    return
                else:
                    fileLineIndex = fileLineIndex - (MMLTAB[macroName] + 1 - checkLevel)
                    return                
            else:
                fileLineIndex = fileLineIndex - (MMLTAB[macroName] + 1 - checkLevel)

            checkLevel -= 1
         
        expandingMacroName = macroName
        
        EXPAND(label, macroName, arguments)
		
    else:
        outputFile.write(line)

def DEFINE(macroDefinedLine):
	# e.g. MACROX	MACRO
	# For macroName, parameters
    
    print(f'MacroDefinedLine => {macroDefinedLine}')
    
    tokens = macroDefinedLine.split()
    macroName = tokens[0]
    macroBody = []
    if len(tokens) == 2:
        parameters = []
    else:
		# parameters is ["&INDEV", "&BUFADR", "&RECLTH"]
        parameters = tokens[2].split(",")
		
    LEVEL = 1
    TEMPTAB[macroName] = LEVEL
    
    while LEVEL > 0:
		# e.g. RDBUFF	MACRO	&ADDR
		# The next line from input file
        line = GETLINE()

        tokens = line.split()
		
        if len(tokens) >= 2 and tokens[1] == 'MACRO':
            LEVEL += 1
            
            for tempMacroName in TEMPTAB.keys():
                TEMPTAB[f'{tempMacroName}'] +=  1
            TEMPTAB[tokens[0]] = 1 
            
        elif len(tokens) == 1 and tokens[0] == 'MEND':
            LEVEL -= 1

        if LEVEL == 0:
            for tempMacroName, macroMaxLevel in TEMPTAB.items():
                MMLTAB[tempMacroName] = macroMaxLevel
            TEMPTAB.clear()
            break
        else:
            print(f'DEFINE Line => {line}')
            replacedLine = positionalNotation(line, parameters)
            macroBody.append(replacedLine)
            		
    #del macroBody[len(macroBody)-1]
	
    DEFTAB[macroName] = macroBody   

    return

def EXPAND(label, macroName, arguments):
    global expandingMacroName
    global expandedLineIndex
	
    macroBody = DEFTAB[macroName]

    print(f'ExpandingMacroName = {expandingMacroName}\n')

    while expandedLineIndex < len(macroBody):
		# e.g. RDBUFF	MACRO	&ADDR
		# The next line of macro definition from DEFTAB
        line = GETLINE()
        
        # The original label is added only if the macro has a label originally
        # and the first line of the macro is traversed.
        if len(label) != 0 and expandedLineIndex == 1 and MMLTAB[macroName] == 1:
            # Replace "\t" with "", and replace no more than once
            line = line.replace("\t", "", 1)
            line = f'{label}{line}'
        
        for i in range(0, len(arguments)):
            line = line.replace(f'PARA{i+1}', arguments[i])

        PROCESSLINE(line)
    
    expandingMacroName = ""
    expandedLineIndex = 0

# Replace   &INDEV,&BUFADR,&RECLTH,     with    PARA1, PARA2, PARA3
def positionalNotation(line, parameters):
    for i in range(0, len(parameters)):
        line = line.replace(parameters[i], f'PARA{i+1}')
    return line
    
def OPcodeisEND(processLine):
    tokens = processLine.split()
    
    # e.g.          END
    if len(tokens) == 1 and tokens[0] == 'END':
        return True
    # e.g.          END     FIRST   or      RECUR   END
    elif len(tokens) == 2 and (tokens[0] == 'END' or tokens[1] == 'END'):
        return True
    # e.g. RECUR    END     FIRST
    elif len(tokens) == 3 and tokens[1] == 'END':
        return True
    else:
        return False

if len(sys.argv) != 2:
    print("Usage: python3 macroprocessor.py <source file>")
    sys.exit()
    
# The Main Program

try:
    with open(sys.argv[1], "r") as fp:
        lines = fp.readlines();
except FileNotFoundError:
    print("\nError：所指定要讀取的 OBJ File 並不存在！\n") 

# Definition Table
# DEFTAB[macroName] = macroBody => {macroName : macroBody}
DEFTAB = {}

# Temporary Multiple Macro Level Table
# TEMPTAB[tempMacroName] = macroMaxLevel => {tempMacroName : macroMaxLevel}
TEMPTAB = {}

# Multiple Macro Level Table
# MMLTAB[macroName] = macroMaxLevel => {macroName : macroMaxLevel}
MMLTAB = {}

outputFile = expandedFile.openFile(sys.argv[1])

expandingMacroName = ""
fileLineIndex = 0
expandedLineIndex = 0
processLine = ""

while OPcodeisEND(processLine) == False:
    processLine = GETLINE()
    print(f'Line{fileLineIndex} : {processLine}')
    PROCESSLINE(processLine)

print(f'\n * Definition Table * \n{DEFTAB}')    
print(f'\n * Multiple Macro Level Table * \n{MMLTAB}')