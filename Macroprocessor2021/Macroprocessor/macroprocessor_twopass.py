import sys
import expandedFile

def Pass1():
    macroFlag = False
    for line in lines:
        
        # if Blank Line or Comment Out Line, continue.
        # The .strip() method is used to remove the characters specified 
        # at the beginning and end of a string (default is a space " " or newline "\n")
        if line[0] == '.' or line.strip() == '':   # Determine whether a line is a comment line or a blank line
            continue
        
        # e.g. RDBUFF   MACRO   &INDEV,&BUFADR,&RECLTH
        tokens = line.split()
        
        # Once "MACRO" is read, a dictionary {macroName(key): macroBody(value)} is created.
        if len(tokens) > 1 and tokens[1] == 'MACRO':
            macroFlag = True
            macroName = tokens[0]
            macroBody = []

            if len(tokens) == 2:
                parameters = []
            else:
                # parameters is ["&INDEV", "&BUFADR", "&RECLTH"]
                parameters = tokens[2].split(",")
                
        # Once "MEND" is read, DEFTAB adds a new definition of Macro.   
        elif len(tokens) == 1 and tokens[0] == 'MEND':
            DEFTAB[macroName] = macroBody
            macroFlag = False
            
        else:
            if macroFlag == True:
                replacedLine = positionalNotation(line, parameters)
                macroBody.append(replacedLine)

# Replace   &INDEV,&BUFADR,&RECLTH,     with    PARA1, PARA2, PARA3
def positionalNotation(line, parameters):
    for i in range(0, len(parameters)):
        line = line.replace(parameters[i], f'PARA{i+1}')
    return line

def Pass2():
    macroFlag = False
    for line in lines:
    
        # if Blank Line or Comment Out Line, continue.
        # The .strip() method is used to remove the characters specified 
        # at the beginning and end of a string (default is a space " " or newline "\n")
        if line[0] == '.' or line.strip() == '':   # Determine whether a line is a comment line or a blank line
            continue
        
        # e.g. RDBUFF   MACRO   &INDEV,&BUFADR,&RECLTH
        tokens = line.split()
    
        if len(tokens) > 1 and tokens[1] == 'MACRO':
            macroFlag = True
        elif len(tokens) == 1 and tokens[0] == 'MEND':
            macroFlag = False
        # End of all macro definitions and access to the main program.
        else:
            if macroFlag == False:
                # Determine whether it is a call of macro
                # e.g. CLOOP    RDBUFF      F1,BUFFER,LENGTH, RDBUFF is tokens[1]
                # e.g.          WRBUFF      05,BUFFER,LENGTH, WRBUFF is tokens[0]
                if tokens[0] in DEFTAB or (len(tokens) >= 2 and tokens[1] in DEFTAB):
                    # e.g.          WRBUFF      05,BUFFER,LENGTH,
                    # WRBUFF is tokens[0]
                    if tokens[0] in DEFTAB:
                        label = ""
                        macroName = tokens[0]
                        arguments = tokens[1].split(",")
                    # e.g. CLOOP    RDBUFF      F1,BUFFER,LENGTH,
                    # RDBUFF is tokens[1]   
                    else:
                        label = tokens[0]
                        macroName = tokens[1]
                        arguments = tokens[2].split(",")
                        
                    expand(label, macroName, arguments)
                else:
                    outputFile.write(line)
                    
def expand(label, macroName, arguments):
    macroBody = DEFTAB[macroName]

    for line in macroBody:
        # The original label is added only if the macro has a label originally
        # and the first line of the macro is traversed.
        if len(label) != 0 and macroBody.index(line) == 0:
            # Replace "\t" with "", and replace no more than once
            line = line.replace("\t", "", 1)
            line = f'{label}{line}'
        
        for i in range(0, len(arguments)):
            line = line.replace(f'PARA{i+1}', arguments[i])
        outputFile.write(line)

if len(sys.argv) != 2:
    print("Usage: python3 macroprocessor.py <source file>")
    sys.exit()
    
# The Main Program
    
try:
    with open(sys.argv[1], "r") as fp:
        lines = fp.readlines();
except FileNotFoundError:
    print("\nError：所指定要讀取的 OBJ File 並不存在！\n")

DEFTAB = {}

outputFile = expandedFile.openFile(sys.argv[1])

Pass1()

print()
for macroName,  macroBody in DEFTAB.items():
    print(macroName, end = '\n\n')
    print(macroBody, end = '\n\n')
    for line in macroBody:
        print(line, end = '\n')
print()

Pass2()