@256
D=A
@SP
M=D
@300
D=A
@LCL
M=D
@400
D=A
@ARG
M=D
@3000
D=A
@THIS
M=D
@3010
D=A
@THAT
M=D
// push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 8
@SP
AM=M-1
D=M
@staticTest.8
M=D
// pop static 3
@SP
AM=M-1
D=M
@staticTest.3
M=D
// pop static 1
@SP
AM=M-1
D=M
@staticTest.1
M=D
// push static 3
@staticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@staticTest.1
D=M
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
// push static 8
@staticTest.8
D=M
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
