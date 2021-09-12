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

(LOOP)
@KBD
D=M

@PRINT
D;JNE

@NPRINT
0;JMP

(PRINT)
@i
M=0
@n
M=0
@8192
D=A
@n
M=M+D
@SCREEN
D=A
@18
M=D

(LOOP2)
@i
D=M
@n
D=D-M
@LOOP
D;JGT
@18
A=M
M=-1
@i
M=M+1
@18
M=M+1
@LOOP2
0;JMP

(NPRINT)
@j
M=0
@m
M=0
@8192
D=A
@m
M=M+D
@SCREEN
D=A
@add
M=D

(LOOP3)
@j
D=M
@m
D=D-M
@LOOP
D;JGT
@add
A=M
M=0
@j
M=M+1
@add
M=M+1
@LOOP3
0;JMP


