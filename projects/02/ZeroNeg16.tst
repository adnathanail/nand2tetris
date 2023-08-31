load ZeroNeg16.hdl,
output-file ZeroNeg16.out,
compare-to ZeroNeg16.cmp,
output-list in%B1.16.1 z%B1.1.1 n%B1.1.1 out%B1.16.1;

set in %B0000000000000000,
set n 0,
set z 0,
eval,
output;

set in %B0110000111000110,
set n 0,
set z 0,
eval,
output;

set in %B0110000111000110,
set n 1,
set z 0,
eval,
output;

set in %B0110000111000110,
set n 0,
set z 1,
eval,
output;

set in %B0110000111000110,
set n 1,
set z 1,
eval,
output;
