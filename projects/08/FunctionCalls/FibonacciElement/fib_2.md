Changed Sys.vm to push constant 2

371 Before call Main.fibonacci 1
SP    262
LCL   261                (0 on vm because they fake the call Sys.init 0)
ARG   256                (0 on vm)
THIS  0
THAT  0
Stack
--------
- 256 51 Return address  (0 on vm)
- 257 0  Saved LCL
- 258 0  Saved ARG
- 259 0  Saved THIS
- 260 0  Saved THAT
- 261 2  Pushed constant



51 After call Main.fibonacci 1
SP    267
LCL   267
ARG   261
THIS  0
THAT  0
Stack
--------
- 256 51  Return address  (0 on vm)
- 257 0   Saved LCL
- 258 0   Saved ARG
- 259 0   Saved THIS
- 260 0   Saved THAT
--------
- 261 2   ARG
- 262 418 Return address  (24 on vm)
- 263 261 Saved LCL       (0 on vm)
- 264 256 Saved ARG       (0 on vm)
- 265 0   Saved THIS
- 266 0   Saved THAT



184 Before recursive call Main.fibonacci 1
SP    268
LCL   267
ARG   261
THIS  0
THAT  0
Stack
--------
- 256 51  Return address  (0 on vm)
- 257 0   Saved LCL
- 258 0   Saved ARG
- 259 0   Saved THIS
- 260 0   Saved THAT
--------
- 261 2   ARG
- 262 418 Return address  (24 on vm)
- 263 261 Saved LCL       (0 on vm)
- 264 256 Saved ARG       (0 on vm)
- 265 0   Saved THIS
- 266 0   Saved THAT
- 267 0



51 After recursive call Main.fibonacci 1
SP    273
LCL   273
ARG   267
THIS  0
THAT  0
Stack
--------
- 256 51  Return address  (0 on vm)
- 257 0   Saved LCL
- 258 0   Saved ARG
- 259 0   Saved THIS
- 260 0   Saved THAT
--------
- 261 2   ARG
- 262 418 Return address  (24 on vm)
- 263 261 Saved LCL       (0 on vm)
- 264 256 Saved ARG       (0 on vm)
- 265 0   Saved THIS
- 266 0   Saved THAT
- 267 0
--------
- 268 418 Return address  (14 on vm)
- 269 267 Saved LCL
- 270 261 Saved ARG
- 271 0   Saved THIS
- 272 0   Saved THAT


WRONG RETURN ADDRESS ^^



108 Before first return
SP    274
LCL   273
ARG   267
THIS  0
THAT  0
Stack
--------
- 256 51  Return address  (0 on vm)
- 257 0   Saved LCL
- 258 0   Saved ARG
- 259 0   Saved THIS
- 260 0   Saved THAT
--------
- 261 2   ARG
- 262 418 Return address  (24 on vm)
- 263 261 Saved LCL       (0 on vm)
- 264 256 Saved ARG       (0 on vm)
- 265 0   Saved THIS
- 266 0   Saved THAT
- 267 0
--------
- 268 418 Return address  (14 on vm)
- 269 267 Saved LCL
- 270 261 Saved ARG
- 271 0   Saved THIS
- 272 0   Saved THAT
- 273 0


418 After first return
SP    268
LCL   267
ARG   261
THIS  0
THAT  0
Stack
--------
- 256 51  Return address  (0 on vm)
- 257 0   Saved LCL
- 258 0   Saved ARG
- 259 0   Saved THIS
- 260 0   Saved THAT
--------
- 261 2   ARG
- 262 418 Return address  (24 on vm)
- 263 261 Saved LCL       (0 on vm)
- 264 256 Saved ARG       (0 on vm)
- 265 0   Saved THIS
- 266 0   Saved THAT
- 267 0