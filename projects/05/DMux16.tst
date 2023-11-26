// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/01/DMux.tst

load DMux16.hdl,
output-file DMux16.out,
compare-to DMux16.cmp,
output-list in%B1.16.1 sel%B3.1.3 a%B1.16.1 b%B1.16.1;

set in %B0000000000000000,
set sel 0,
eval,
output;

set in %B0000000000000001,
eval,
output;

set in %B1001010000000001,
set sel 1,
eval,
output;
