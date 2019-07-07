// push constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop local 0
@LCL
D=M
@0
D=D+A
@SP
M=M-1
A=M
D=M
@0
M=D
// push constant 21
@21
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 22
@22
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop argument 2
// pop argument 1
// push constant 36
@36
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop this 6
// push constant 42
@42
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 45
@45
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 5
// pop that 2
// push constant 510
@510
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop temp 6
// push local 0
// push that 5
// add
// push argument 1
// sub
// push this 6
// push this 6
// add
// sub
// push temp 6
// add
