// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Initialise screen colour as white
    @R2
    M=0
// Keep checking the keyboard input and, if the input is greater than 0, jump to FILL
(LOOP)
    @KBD
    D=M
    @FILLBLACK
    D;JGT

    @R2
    D=M
    @FILLWHITE
    D; JLT

    @LOOP
    0;JMP

(FILLBLACK)
    @R2
    M=-1
    @FILL
    0;JMP
(FILLWHITE)
    @R2
    M=0
    @FILL
    0;JMP
(FILL)
    // Reset R1 to start of screen
    @SCREEN
    D=A
    @R1
    M=D-1
(FILLLOOP)
    @R2
    D=M
    @R1
    M=M+1
    A=M
    M=D
    @R1
    D=M
    @24575 // Last screen memory location
    D=A-D
    // If we are at the end of the screen return to the loop
    @LOOP
    D;JEQ
    @FILLLOOP
    0;JMP