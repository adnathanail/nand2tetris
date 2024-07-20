Changed Sys.vm to push constant 1
SP correctly ends at 261
261 correctly contains 1


19 Before call Sys.init 0
SP    256
LCL   -1
ARG   -2
THIS  -3
THAT  -4


66 After call Sys.init 0
SP    261
LCL   261
ARG   256
THIS  -3
THAT  -4
Stack
--------
- 256 67  Return address
- 257 -1  Saved LCL
- 258 -2  Saved ARG
- 259 -3  Saved THIS
- 260 -4  Saved THAT
--------


433 After call Main.fibonacci 1
SP    267
LCL   267
ARG   261
THIS  -3
THAT  -4
Stack
---------
- 256  67 Return address
- 257  -1 Saved LCL
- 258  -2 Saved ARG
- 259  -3 Saved THIS
- 260  -4 Saved THAT
---------
- 261   1 ARG
- 262 434 Return address
- 263 261 Saved LCL
- 264 256 Saved ARG
- 265  -3 Saved THIS
- 266  -4 Saved THAT
---------


123 Before Main.fibonacci return
SP    268
LCL   267
ARG   261
THIS  -3
THAT  -4
Stack
---------
- 256  67 Return address
- 257  -1 Saved LCL
- 258  -2 Saved ARG
- 259  -3 Saved THIS
- 260  -4 Saved THAT
---------
- 261   1 ARG
- 262 434 Return address
- 263 261 Saved LCL
- 264 256 Saved ARG
- 265  -3 Saved THIS
- 266  -4 Saved THAT
---------
- 267   1 Return value


171 After Main.fibonacci return
SP    262
LCL   261
ARG   256
THIS  -3
THAT  -4
Stack
---------
- 256  67 Return address
- 257  -1 Saved LCL
- 258  -2 Saved ARG
- 259  -3 Saved THIS
- 260  -4 Saved THAT
---------
- 261   1 Returned from Main.fibonacci
