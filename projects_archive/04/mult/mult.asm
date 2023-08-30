// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    // Initialise sum and tally
    @R2 // Sum
    M=0
    @R3 // Tally
    M=0

(LOOP)
    // Go to end if Tally==R0 i.e. multiplcation complete
    @R0
    D=M
    @R3
    D=D-M
    @END
    D;JLE

    // Add R1 to total and go back to loop
    @R1
    D=M
    @R2 // Total
    M=M+D
    @R3 // Tally
    M=M+1
    @LOOP
    0;JMP

(END)
    @END
    0;JMP