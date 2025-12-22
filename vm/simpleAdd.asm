@256
D=A
@SP
M=D
//push command
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
//push command
@8
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
