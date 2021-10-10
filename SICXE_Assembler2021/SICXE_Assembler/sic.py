OPTAB = {

    # SIC Instruction Set
    
    "ADD":   0x18,
    "AND":   0x40,
    "COMP":  0x28,
    "DIV":   0x24,
    "J":     0x3C,
    "JEQ":   0x30,
    "JGT":   0x34,
    "JLT":   0x38,
    "JSUB":  0x48,
    "LDA":   0x00,
    "LDCH":  0x50,
    "LDL":   0x08,
    "LDX":   0x04,
    "MUL":   0x20,
    "OR":    0x44,
    "RD":    0xD8,
    "RSUB":  0x4C,
    "STA":   0x0C,
    "STCH":  0x54,
    "STL":   0x14,
    "STSW":  0xE8,
    "STX":   0x10,
    "SUB":   0x1C,
    "TD":    0xE0,
    "TIX":   0x2C,
    "WD":    0xDC,
    
    # SIC/XE Instruction Set
    
    "ADDF":  0x58,
    "ADDR":  0x90,
    "CLEAR": 0xB4,
    "COMPF": 0x88,
    "COMPR": 0xA0,
    "DIVF":  0x64,
    "DIVR":  0x9C,
    "FIX":   0xC4,
    "FLOAT": 0xC0,
    "HIO":   0xF4,
    "LDB":   0x68,
    "LDF":   0x70,
    "LDS":   0x6C,
    "LDT":   0x74,
    "LPS":   0xD0,
    "MULF":  0x60,
    "MULR":  0x98,
    "NORM":  0xC8,
    "RMO":   0xAC,
    "SHIFTL":0xA4,
    "SHIFTR":0xA8,
    "SIO":   0xF0,
    "SSK":   0xEC,
    "STB":   0x78,
    "STF":   0x80,
    "STI":   0xD4,
    "STS":   0x7C,
    "STT":   0x84,
    "SUBF":  0x5C,
    "SUBR":  0x94,
    "SVC":   0xB0,
    "TIO":   0xF8,
    "TIXR":  0xB8
}

REGISTERS = {

    # SIC Registers
    
    "A":    0,
    "X":    1,
    "L":    2,
    "PC":   8,
    "SW":   9,

    # SIC/XE Registers

    "B":    3,
    "S":    4,
    "T":    5,
    "F":    6
}

def isInstruction(token):
    if token in OPTAB:
        return True
    else:
        return False