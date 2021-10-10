import objreader

def execute(ESTAB, PROGADDR, PROG):
    # Control Section Address
    CSADDR = PROGADDR
    
    # 記憶體空間
    MemorySpace = 0

    for i in range(0, len(PROG)):
        lines = objreader.readOBJFiles(PROG[i])
        
        # Header Record
        # Col. 2-7: Program name
        # Col. 8-13: Starting address (hexadecimal)
        # Col. 14-19 Length of object program in bytes
        Hline = objreader.readRecordWithoutSpace(lines[0])  # Replace All Space for Header Line
        CSNAME = Hline[1:6]
        CSLTH  = int(f'{Hline[12:18]}', 16)                 # 將 Address 從 string 更改成 hex digit

        MemorySpace += CSLTH

        ESTAB[CSNAME] = CSADDR
        
        for j in range(1, len(lines)):
            # Define Record
            # Col. 2-7: Name of external symbol defined in this control section
            # Col. 8-13: Relative address of symbol within this control section
            if lines[j][0] == 'D':
                ExternalSymbolNumbers = int((len(lines[j]) - 1) / 12)                       # -1: lines[j][0] = 'D'
                
                for k in range(0, ExternalSymbolNumbers): 
                    ESNAME = objreader.readRecordWithoutSpace(lines[j][1+(12*k):7+(12*k)])  # Replace All Space for Define Line
                    ESADDR = int(f'{lines[j][7+(12*k):13+(12*k)]}', 16)                     # 將 Address 從 string 更改成 hex digit
                    ESTAB[ESNAME] = CSADDR + ESADDR
        
        CSADDR += CSLTH
            
    return MemorySpace