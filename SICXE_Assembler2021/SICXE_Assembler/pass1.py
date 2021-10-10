import sic
import common

SYMTAB = {}

def execute(tokenslist):
    LOCCTR = 0                  # Location Counter
    if tokenslist[0][0] == "START":
        LOCCTR = int(tokenslist[0][1], 16)
    elif tokenslist[0][1] == "START":
        LOCCTR = int(tokenslist[0][2], 16)
    STARTING = LOCCTR
    
    for i in range(1, len(tokenslist)):
    
        opcode = tokenslist[i][0]
        
        if opcode == "END":
            PROGLEN = LOCCTR - STARTING
            break

        if opcode == "BASE":    # Location Counter isn't changed
            continue;
            
        # ['Label', 'Opcode', 'Operand'] or ['Label', 'Opcode']
        if common.hasLabel(tokenslist[i]):
            label = opcode
            opcode = tokenslist[i][1]
            if len(tokenslist[i]) == 3:
                operand = tokenslist[i][2]
            
            if label in SYMTAB:
                print("Source Code has an erros: duplicate lables")
                return -1
            SYMTAB[label] = LOCCTR
        # ['Opcode', 'Operand'] or ['Opcode']
        else:
            if len(tokenslist[i]) == 2:
                operand = tokenslist[i][1] 
        
        if opcode in sic.OPTAB:
            
            operandlist =  operand.replace(',', ' ').split()
            
            # e.g. Operand = ['A', 'S']
            if len(operandlist) == 2:
                # Format2
                if operandlist[0] in sic.REGISTERS and operandlist[1] in sic.REGISTERS:
                    LOCCTR += 2
                # Format3    
                else:
                    LOCCTR += 3
            # e.g. Operand = ['X']        
            elif len(operandlist) == 1:
                # Format2
                if operandlist[0] in sic.REGISTERS:
                    LOCCTR += 2
                # Format3
                else:
                    LOCCTR += 3
            # if len(operandlist) == 0: Format3 
            else:
                LOCCTR += 3
        
        # Format4
        elif opcode[0] == '+' and opcode[1:] in sic.OPTAB:
            LOCCTR += 4
            
        elif opcode == "WORD":
            LOCCTR += 3
            
        elif opcode == "BYTE":

            operand = tokenslist[i][2]
            if operand[0] == 'X':
                operandlen = int((len(operand) - 3)/2)
            elif operand[0] == 'C':
                operandlen = int(len(operand) - 3)
                                 
            LOCCTR += operandlen
            
        elif opcode == "RESB":
            operandval = int(tokenslist[i][2])
            LOCCTR += operandval
            
        elif opcode == "RESW":
            operandval = int(tokenslist[i][2])
            LOCCTR += (operandval * 3)
            
        else:
            print("Invalid Instruction / Invalid Directive")
            print(opcode, operand)
            return -2;    
        
    return (LOCCTR-STARTING)