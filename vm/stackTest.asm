@256
D=A
@SP
M=D
//push command
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_TRUE1
D;JEQ
@SP
A=M-1
M=0
@EQ_END1
0;JMP
(EQ_TRUE1)
@SP
A=M-1
M=-1
(EQ_END1)
//push command
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_TRUE2
D;JEQ
@SP
A=M-1
M=0
@EQ_END2
0;JMP
(EQ_TRUE2)
@SP
A=M-1
M=-1
(EQ_END2)
//push command
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_TRUE3
D;JEQ
@SP
A=M-1
M=0
@EQ_END3
0;JMP
(EQ_TRUE3)
@SP
A=M-1
M=-1
(EQ_END3)
//push command
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LT_TRUE4
D;JLT
@SP
A=M-1
M=0
@LT_END4
0;JMP
(LT_TRUE4)
@SP
A=M-1
M=-1
(LT_END4)
//push command
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LT_TRUE5
D;JLT
@SP
A=M-1
M=0
@LT_END5
0;JMP
(LT_TRUE5)
@SP
A=M-1
M=-1
(LT_END5)
//push command
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@LT_TRUE6
D;JLT
@SP
A=M-1
M=0
@LT_END6
0;JMP
(LT_TRUE6)
@SP
A=M-1
M=-1
(LT_END6)
//push command
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_TRUE7
D;JGT
@SP
A=M-1
M=0
@GT_END7
0;JMP
(GT_TRUE7)
@SP
A=M-1
M=-1
(GT_END7)
//push command
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_TRUE8
D;JGT
@SP
A=M-1
M=0
@GT_END8
0;JMP
(GT_TRUE8)
@SP
A=M-1
M=-1
(GT_END8)
//push command
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_TRUE9
D;JGT
@SP
A=M-1
M=0
@GT_END9
0;JMP
(GT_TRUE9)
@SP
A=M-1
M=-1
(GT_END9)
//push command
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
//Add command
@SP
AM=M-1
D=M
A=A-1
M=D+M
//push command
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=D&M
//push command
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
A=A-1
M=D|M
// not
@SP
A=M-1
M=!M
