// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// R2 = 0
@2
M=0
// i = R1
@1
D=M
@i
M=D
(LOOP)
// if i == 0 goto END
@i
D=M
@END
D;JEQ
// R2 += R0
@0
D=M
@2
M=M+D
// i -= 1
@i
M=M-1
// goto LOOP
@LOOP
0;JMP

(END)