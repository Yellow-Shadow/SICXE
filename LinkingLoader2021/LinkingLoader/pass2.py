import objreader


def hexDig2hexStr(hexDig, length):
    hexDig = hexDig.upper()
    hexStr = hexDig[2:]                         # 0xFFFFF6 => FFFFF6
    for i in range(0, length - len(hexStr)):    # 位數不足補零
        hexStr = '0' + hexStr
    return hexStr
    
# Hex String => Dec Int Digit
def hexStr2decDig(hexStr, bits):
    decDig = int(hexStr, 16)                    # 0xFFFFF6 => 16777206
    if decDig & (1 << (bits-1)):                # 2^0 << (bits-1) =  0x800000 =>  8388608
        decDig -= 1 << (bits)					# Threshold Of Negative Number：Negative decDig > 7FFFFF >= Positive decDig    
												# 2^0 << (bits)   = 0x1000000 => 16777216
#    if decDig >= int(pow(2, bits-1)):
#        decDig -= int(pow(2, bits))
    return decDig
    
# Dec Int Digit => Hex Int Digit
def decDig2hexDig(decDig, bits):
    return hex((decDig + (1 << bits)) % (1 << bits))
                                                # e.g. hex[(-10 + 256) % 256] = 0xF6
                                                # e.g. hex[( 10 + 256) % 256] = 0x0A
# Text Record
# Col.  2-7: Starting address for object code in this record
# Col.  8-9: Length of object code in this record in bytes
# e.g.   0A: 10 bytes (20 half-bytes)
# Col.10-69: Object code
def processTRecord(Tline, CSADDR, PROGADDR, MemoryContent):
    TADDR  = int(f'0x{Tline[1:7]}', 16)         # 將 Address 從 string 更改成 hex digit
    TADDR += CSADDR
    TADDR -= PROGADDR
    TADDR *= 2                                  # 將 1byte (Binary) 用 2個 數字(HEX)表示, 故需要將 Address 兩倍
                                                # e.g. 1011 0110 => B6
    
    length = int(f'0x{Tline[7:9]}', 16)         # 將 Length 從 string 更改成 hex digit
    
    for i in range(0, length * 2):              # bytes = half-bytes * 2
        MemoryContent[TADDR] = Tline[9 + i]     # 將 Object code 照著 TADDR 的順序, 依序填入 MemoryContent 中
        TADDR += 1

# Modification Record
# Col.   2-7: Starting location of the address field to be modified, relative to the beginning of the program
# Col.   8-9: Length of the address field to be modified (half-bytes)
# Col.    10: Modification flag (+ or -)
# Col. 11-16: External symbol whose value is to be added to or subtracted from the indicated field
def processMRecord(Mline, CSADDR, PROGADDR, MemoryContent, ESTAB):
    MADDR  = int(f'0x{Mline[1:7]}', 16)         # 將 Address 從 string 更改成 hex digit
    MADDR += CSADDR
    MADDR -= PROGADDR
    MADDR *= 2                                  # 將 1byte (Binary) 用 2個 數字(HEX)表示, 故需要將 Address 兩倍
                                                # e.g. 1011 0110 => B6
    
    length = int(f'0x{Mline[7:9]}', 16)         # 將 Length 從 string 更改成 hex digit
    
    if (length == 5):                           # "05"代表除了需要跳過 First Byte(OPCODE + n,i) 
         MADDR += 1                             # 還需要跳過 Second Half-Byte(x,b,p,e)  
                                                # e.g."77100004" 跳過 "77" 與 "1", address field 才是 "00004" 
    
    # FFFFF6 = ['F', 'F', 'F', 'F', 'F', '6']
    current = "".join(MemoryContent)[MADDR:MADDR + length]
    
    # -10 = hexStr2decDig(0xFFFFF6, 24)
    decDig = hexStr2decDig(f'0x{current}', length * 4)
    
    # Mline 以 '\n' 結尾，故 token 的擷取位置是從 10 到 len(Mline)-1
    key = Mline[10:len(Mline)-1]
    
    if Mline[9] == '+':
        decDig += ESTAB[key]
    else:
        decDig -= ESTAB[key]
    
    modifiedHexStr = hexDig2hexStr(decDig2hexDig(decDig, length * 4), length)

    for i in range(0, length):                  # 將更改後的 modifiedHexStr 照著 MADDR 的順序, 依序填入 MemoryContent 中
        MemoryContent[MADDR] = modifiedHexStr[i]
        MADDR += 1

def execute(ESTAB, PROGADDR, PROG, MemoryContent):
    # Control Section Address
    CSADDR = PROGADDR
        
    for i in range(0, len(PROG)):
        lines = objreader.readOBJFiles(PROG[i])
        
        # Header Record
        # Col. 2-7: Program name
        # Col. 8-13: Starting address (hexadecimal)
        # Col. 14-19 Length of object program in bytes
        Hline = objreader.readRecordWithoutSpace(lines[0])  # Replace All Space for Header Line
        # CSNAME = Hline[1:6]
        CSLTH  = int(f'{Hline[12:18]}', 16)                 # 將 Address 從 string 更改成 hex digit

        for j in range(1, len(lines)):
            # Text Record
            if lines[j][0] == 'T':
                processTRecord(lines[j], CSADDR, PROGADDR, MemoryContent)
            # Modification Record
            if lines[j][0] == 'M':
                processMRecord(lines[j], CSADDR, PROGADDR, MemoryContent, ESTAB)
                
        CSADDR += CSLTH
