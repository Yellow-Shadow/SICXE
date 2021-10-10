import sic
import common
import objfile

modification = []

def execute(filename, tokenslist, SYMTAB, proglen):

    file = objfile.openFile(filename)
    
    LOCCTR = 0
    if tokenslist[0][0] == "START":
        LOCCTR = int(tokenslist[0][1], 16)
        name = ""
    elif tokenslist[0][1] == "START":
        LOCCTR = int(tokenslist[0][2], 16)
        name = tokenslist[0][0]
    STARTING = LOCCTR

    objfile.writeHeader(file, name, STARTING, proglen)

    tline = ""              # Initialize tline
    tstart = LOCCTR
    BASE = 0                # Initialize BASE
    instruction = ""        # Initialize instruction

    for i in range(1, len(tokenslist)):
        
        if tokenslist[i][0] == "END":
            
            if len(tline) > 0:                
                objfile.writeText(file, tstart, tline)
            
            PROGLEN = LOCCTR - STARTING

            address = STARTING
                           
            objfile.writeModification(file, modification)
            
            if len(tokenslist[i]) == 2:
                address = SYMTAB[tokenslist[i][1]]
            
            objfile.writeEnd(file, address)            
            break

        
        # If Opcode is "BASE", Location Counter isn't changed
        # Meantime, calculating the value of BASE
        if tokenslist[i][0] == "BASE":
            if tokenslist[i][1].isdigit() == True:
                BASE = int(tokenslist[i][1])
            else:
                BASE = SYMTAB[tokenslist[i][1]]
            continue
        
        label = ""
        opcode = tokenslist[i][0]
        operand = ""

        
        # ['Label', 'Opcode', 'Operand'] or ['Label', 'Opcode']
        if common.hasLabel(tokenslist[i]):
            label = opcode
            opcode = tokenslist[i][1]
            if len(tokenslist[i]) == 3:
                operand = tokenslist[i][2]
        # ['Opcode', 'Operand'] or ['Opcode']
        else:
            if len(tokenslist[i]) == 2:
                operand = tokenslist[i][1]
        
        
        # For the Format3 and For the Format4 (e.g. +JSUB)       
        if opcode in sic.OPTAB or opcode[1:] in sic.OPTAB:

            operandlist =  operand.replace(',', ' ').split()
            
            # Format4
            if opcode[0] == '+' and opcode[1:] in sic.OPTAB:
                instruction = generateInstructionFormat4(opcode, operand, SYMTAB, LOCCTR, BASE)

            # Format2 e.g. Operand = ['X']
            elif len(operandlist) == 1 and operandlist[0] in sic.REGISTERS:
                instruction = generateInstructionFormat1or2(opcode, operand, SYMTAB, LOCCTR, BASE)

            # Format2 e.g. Operand = ['A', 'S']
            elif len(operandlist) == 2 and operandlist[0] in sic.REGISTERS and operandlist[1] in sic.REGISTERS:
                instruction = generateInstructionFormat1or2(opcode, operand, SYMTAB, LOCCTR, BASE)
            
            # Format3
            else:
                instruction = generateInstructionFormat3(opcode, operand, SYMTAB, LOCCTR, BASE)

#            print(instruction)
#            print(len(instruction))
            
            if len(instruction) == 0:
                print("Undefined Symbole: %s" % operand)
                return -1
            
            if LOCCTR + (len(instruction)/2) - tstart > 30:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = instruction
            else:
                tline += instruction
                
            # Format4    
            if opcode[0] == '+':
                LOCCTR += 1

            # Format2 e.g. Operand = ['X']               
            elif len(operandlist) == 1 and operandlist[0] in sic.REGISTERS:
                LOCCTR -= 1
                
            # Format2 e.g. Operand = ['A', 'S']                
            elif len(operandlist) == 2 and operandlist[0] in sic.REGISTERS and operandlist[1] in sic.REGISTERS:
                LOCCTR -= 1
                
            LOCCTR += 3
            
        elif opcode == "WORD":

            constant = objfile.hexstrToWord(hex(int(operand)))

            if LOCCTR + 3 - tstart > 30:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = constant
            else:
                tline += constant
            
            LOCCTR += 3
            
        elif opcode == "BYTE":

            if operand[0] == 'X':
                operandlen = int((len(operand) - 3)/2)
                constant = operand[2:len(operand)-1]
            elif operand[0] == 'C':
                operandlen = int(len(operand) - 3)
                constant = processBYTEC(operand)
            
            if LOCCTR + operandlen - tstart > 30:
                objfile.writeText(file, tstart, tline)
                tstart = LOCCTR
                tline = constant
            else:
                tline += constant            

            LOCCTR += operandlen
            
        elif opcode == "RESB":
            operandval = int(operand)
            LOCCTR += operandval
            
        elif opcode == "RESW":
            operandval = int(operand)
            LOCCTR += (operandval * 3)
            
        else:
            print("Invalid Instruction / Invalid Directive")
            print(opcode, operand)
            return -2 
    
    return (LOCCTR-STARTING)

def processBYTEC(operand):
    constant = ""
    for i in range(2, len(operand)-1):
        tmp = hex(ord(operand[i]))
        tmp = tmp[2:]
        if len(tmp) == 1:
            tmp = "0" + tmp
        tmp = tmp.upper()
        constant += tmp
    return constant

# Format1 (1 bytes) : [op]         => [8]
# Format2 (2 bytes) : [op, r1, r2] => [8, 4, 4]
def generateInstructionFormat1or2(opcode, operand, SYMTAB, LOCCTR, BASE):
    
    instruction = sic.OPTAB[opcode] * 256             # 2^7 # op
    
    if len(operand) > 0:
        operandlist =  operand.replace(',', ' ').split()
        
        instruction += sic.REGISTERS[operandlist[0]] * 16 # 2^4 # r1
        
        if len(operandlist) == 2:
            instruction += sic.REGISTERS[operandlist[1]]        # r2
    
    return objfile.hexstrToWord(hex(instruction))[4:] # 8 - (2 * 8 / 4)
    
    
# Format3 (3 bytes) : [op, n, i, x, b, p, e, disp] => [6, 1, 1, 1, 1, 1, 1, 12]
def generateInstructionFormat3(opcode, operand, SYMTAB, LOCCTR, BASE):
    
    instruction = sic.OPTAB[opcode] * 65536           # 2^16 # op
    
    if len(operand) > 0:
        if operand[len(operand)-2:] == ',X':          # x = 1
            instruction += 32768                      # 2^15
            operand = operand[:len(operand)-2]
            
        if operand[0] == '#':                         # n = 0, i = 1
            instruction += 65536                      # 2^16
            
            if operand[1:].isdigit() == True:
                instruction += int(operand[1:])              # disp   
            else:
                # disp = Target Address -  Program Counter
                disp = SYMTAB[operand[1:]] - (LOCCTR + 3)
                
                # Program-Counter Relative Addressing
                if -2048 <= disp and disp <= 2047:
                    # 利用補碼運算就能不判斷 disp 正數或負數
                    instruction += (disp & 0b111111111111)
                    instruction += 8192               # 2^13 # b = 0, p = 1
                
                # Base Relative Addressing
                else:
                    disp = SYMTAB[operand[1:]] - BASE
                    instruction += disp
                    instruction += 16384              # 2^14 # b = 1, p = 0
            
        elif operand[0] == '@':                       # n = 1, i = 0
            instruction += 131072                     # 2^17  
            
            if operand[1:].isdigit() == True:
                instruction += int(operand[1:])              # disp   
            else:
                # disp = Target Address -  Program Counter
                disp = SYMTAB[operand[1:]] - (LOCCTR + 3)
                
                # Program-Counter Relative Addressing
                if -2048 <= disp and disp <= 2047:
                    # 利用補碼運算就能不判斷 disp 正數或負數
                    instruction += (disp & 0b111111111111)
                    instruction += 8192               # 2^13 # b = 0, p = 1
                
                # Base Relative Addressing
                else:
                    # disp = Target Address -  Base
                    disp = SYMTAB[operand[1:]] - BASE
                    instruction += disp
                    instruction += 16384              # 2^14 # b = 1, p = 0 
                
        else:                                         # n = 1, i = 1
            instruction += 196608                     # 2^16 + 2^17
            
            # disp = Target Address -  Program Counter
            disp = SYMTAB[operand] - (LOCCTR + 3)
            
            # Program-Counter Relative Addressing
            if -2048 <= disp and disp <= 2047:
                # 利用補碼運算就能不判斷 disp 正數或負數
                instruction += (disp & 0b111111111111)
                instruction += 8192                   # 2^13 # b = 0, p = 1
            
            # Base Relative Addressing
            else:
                # disp = Target Address -  Base
                disp = SYMTAB[operand] - BASE
                instruction += disp
                instruction += 16384                  # 2^14 # b = 1, p = 0
        
    else:                                             # n = 1, i = 1
        instruction += 196608                         # 2^16 + 2^17
    
    return objfile.hexstrToWord(hex(instruction))[2:] # 8 - (3 * 8 / 4)

# Format4 (4 bytes) : [op, n, i, x, b, p, e, address] => [6, 1, 1, 1, 1, 1, 1, 20]
def generateInstructionFormat4(opcode, operand, SYMTAB, LOCCTR, BASE):
    
    instruction = sic.OPTAB[opcode[1:]] * 16777216    # 2^24 # op
    
    instruction += 1048576                            # 2^20 # e = 1 
    
    if len(operand) > 0:
        if operand[len(operand)-2:] == ',X':          # x = 1
            instruction += 8388608                    # 2^23
            operand = operand[:len(operand)-2]
            
        if operand[0] == '#':                         # n = 0, i = 1
            instruction += 16777216                   # 2^24
            
            if operand[1:].isdigit() == True:
                instruction += int(operand[1:])              # disp
            else:
                # disp(PC) = Target Address -  Program Counter
                dispPC = SYMTAB[operand[1:]] - (LOCCTR + 4)
                
                # disp(B) = Target Address -  Program Counter
                dispB = SYMTAB[operand[1:]] - BASE 
                                
                # Program-Counter Relative Addressing
                if -2048 <= dispPC and dispPC <= 2047:
                    # 利用補碼運算就能不判斷 disp 正數或負數
                    instruction += (dispPC & 0b111111111111)
                    instruction += 2097152            # 2^21 # b = 0, p = 1
                
                # Base Relative Addressing
                elif 0 <= dispB and dispB <= 4095:
                    instruction += dispB
                    instruction += 4194304            # 2^22 # b = 1, p = 0
                else:
                    instruction += SYMTAB[operand]           # b = 0, p = 0
            
        elif operand[0] == '@':                       # n = 1, i = 0
            instruction += 33554432                   # 2^25
            
            if operand[1:].isdigit() == True:
                instruction += int(operand[1:])              # disp
            else:
                # disp(PC) = Target Address -  Program Counter
                dispPC = SYMTAB[operand[1:]] - (LOCCTR + 4)
                
                # disp(B) = Target Address -  Program Counter
                dispB = SYMTAB[operand[1:]] - BASE 
                                
                # Program-Counter Relative Addressing
                if -2048 <= dispPC and dispPC <= 2047:
                    # 利用補碼運算就能不判斷 disp 正數或負數
                    instruction += (dispPC & 0b111111111111)
                    instruction += 2097152            # 2^21 # b = 0, p = 1
                
                # Base Relative Addressing
                elif 0 <= dispB and dispB <= 4095:
                    instruction += dispB
                    instruction += 4194304            # 2^22 # b = 1, p = 0
                else:
                    instruction += SYMTAB[operand]           # b = 0, p = 0
                
        else:                                         # n = 1, i = 1
            instruction += 50331648                   # 2^24 + 2^25
            
            modification.append(LOCCTR + 1)           # ???
            
            if operand[1:].isdigit() == True:
                instruction += int(operand[1:])              # disp
            else:
                # disp(PC) = Target Address -  Program Counter
                dispPC = SYMTAB[operand] - (LOCCTR + 4)
                
                # disp(B) = Target Address -  Program Counter
                dispB = SYMTAB[operand] - BASE 
                                
                # Program-Counter Relative Addressing
                if -2048 <= dispPC and dispPC <= 2047:
                    # 利用補碼運算就能不判斷 disp 正數或負數
                    instruction += (dispPC & 0b111111111111)
                    instruction += 2097152            # 2^21 # b = 0, p = 1
                
                # Base Relative Addressing
                elif 0 <= dispB and dispB <= 4095:
                    instruction += dispB
                    instruction += 4194304            # 2^22 # b = 1, p = 0
                else:
                    instruction += SYMTAB[operand]           # b = 0, p = 0
                    
    else:                                             # n = 1, i = 1
        instruction += 50331648                       # 2^24 + 2^25            
    
    return objfile.hexstrToWord(hex(instruction)) # 8 - (4 * 8 / 4)