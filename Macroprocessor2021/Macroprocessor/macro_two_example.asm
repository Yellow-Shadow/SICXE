RECUR	START	0
.
MACROX	MACRO
RDBUFF	MACRO	&ADDR
		LDT		&ADDR
		MEND
		MEND
		
MACROS	MACRO
RDBUFF	MACRO	&ADDR
		LDA		&ADDR
		MEND
		MEND
.
FIRST	LDA		THREE
		MACROX
		RDBUFF	FIVE
THREE	WORD	3
FIVE	WORD	5
		END		FIRST