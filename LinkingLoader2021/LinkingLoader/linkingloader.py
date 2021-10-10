import pass1
import pass2
import os

# Input Program Load Address
while True:
    try:
        PROGADDR = input("Please input the beginning address in memory of your linked program：")
        if PROGADDR.isdigit() == 0:
            raise ValueError
        else:
            break
    except ValueError:
        print("\nError：Please input a positive integer.\n")

PROGADDR= int(f'{PROGADDR}', 16)                        # 將 Address 從 string 更改成 hex digit

# Input OBJ Files Name  
PROG = []

dirPath = r"D:\Desktop\海海人生\大三下系統程式\LinkingLoader2021\LinkingLoader"
FilesName = os.listdir(dirPath)

while True:
    try:
        objFileName = input("Please input your complete obj Files name(If you are finished, please input \"END\")：")
        if objFileName == "END":
            break;
        elif objFileName.endswith('.obj') == 0:
            raise TypeError
        elif objFileName not in FilesName:
            raise NameError
        else:
            PROG.append(objFileName)
    except TypeError:
        print("\nError：Please input an accurate obj Files name.\n")
    except NameError:
        print("\nError：Please input an existing obj Files name.\n")
    else:
        print(f'\nThe specified OBJ file 【{objFileName}】 was read successfully！\n')
        
ESTAB = {}

MemorySpace = pass1.execute(ESTAB, PROGADDR, PROG)

print()
for key in ESTAB:
    if key.startswith('PROG'):
        print(f'Control Section：{key} \t Address：0x{hex(ESTAB[key])[2:6].upper()}')
    else:
        print(f'Symbol Name    ：{key} \t Address：0x{hex(ESTAB[key])[2:6].upper()}')
print()

MemoryContent = []

# 將 1byte (Binary) 用 2個 數字(HEX)表示, 故需要將 MemorySpace 擴大兩倍
# e.g. 1011 0110 => B6
for i in range(0, (2 * MemorySpace)):
    MemoryContent.append(".")

pass2.execute(ESTAB, PROGADDR, PROG, MemoryContent)

for i in range(0, (2 * MemorySpace)):
    if i % 32 == 0:
        print(f'\n{pass2.hexDig2hexStr(hex(PROGADDR + int(i/2)), 4)} ', end = "")
        print(f'{MemoryContent[i]}', end = " ")
    elif i % 8 == 0:
        print(f'  {MemoryContent[i]}', end = " ")
    else:
        print(f'{MemoryContent[i]}', end = " ")
print()