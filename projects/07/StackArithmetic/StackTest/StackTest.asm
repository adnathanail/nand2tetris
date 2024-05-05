// SP = 256
@256
D=A
@SP
M=D
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@EQT0
D;JEQ
@SP
A=M
M=0
@EQC0
0;JMP
(EQT0)
@SP
A=M
M=1
(EQC0)
@SP
M=M+1