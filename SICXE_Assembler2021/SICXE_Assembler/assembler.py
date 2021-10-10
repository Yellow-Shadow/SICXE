import sys

import sicasmparser
import pass1
import pass2
import objfile

if len(sys.argv) != 2:
    print("Usage: python3 assembler.py <source file>")
    sys.exit()
    
lines = sicasmparser.readfile(sys.argv[1])

if lines == None:
    print("Cannot open '%s'." % sys.argv[1])
    sys.exit()

tokenslist = sicasmparser.removeCommentLineAndGetTokens(lines)

#print("Tokenlist = \n", tokenslist)

proglen = pass1.execute(tokenslist)

if proglen < 0:
    sys.exit()

#print("PASS1.SYMTAB = \n", pass1.SYMTAB)

proglen = pass2.execute(sys.argv[1], tokenslist, pass1.SYMTAB, proglen)

if proglen > 0:
    print("The obj file was generated successfully!.")