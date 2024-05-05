// SP = 256
@256
D=A
@SP
M=D
// LCL = 300
@300
D=A
@LCL
M=D
// ARG = 400
@400
D=A
@ARG
M=D
// THIS = 3000
@3000
D=A
@THIS
M=D
// THAT = 3010
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
@24
D=A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// pop static 3
@19
D=A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// pop static 1
@17
D=A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
// push static 3
@19
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 1
@17
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
// push static 8
@24
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1