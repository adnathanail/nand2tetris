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

// black = 1111111111111111
@32767
D=A+1
D=A+D
@black
M=D

(LOOP)
// if keyboard == 0 goto WHITE
@KBD
D=M
@BLACK
D;JGT
@WHITE
0;JMP

(BLACK)
// pointer = SCREEN
@SCREEN
D=A
@pointer
M=D
(BLACKLOOP)
// Set @pointer pixel to @black
@black
D=M
@pointer
A=M
M=D
// @pointer += 1
A=A+1
D=A
@pointer
M=D
// if pointer < 24576 goto LOOP
@24576
D=A
@pointer
D=D-M
@BLACKLOOP
D;JGT
@LOOP
0;JMP

(WHITE)
// pointer = SCREEN
@SCREEN
D=A
@pointer
M=D
(WHITELOOP)
// Set @pointer pixel to white
@pointer
A=M
M=0
// @pointer += 1
A=A+1
D=A
@pointer
M=D
// if pointer < 24576 goto LOOP
@24576
D=A
@pointer
D=D-M
@WHITELOOP
D;JGT
@LOOP
0;JMP