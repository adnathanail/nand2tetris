// SP = 256
@256                         // line 0
D=A                          // line 1
@SP                          // line 2
M=D                          // line 3
// call Sys.init 0
@Sys.init.1.return           // line 4
D=A                          // line 5
@SP                          // line 6
A=M                          // line 7
M=D                          // line 8
@SP                          // line 9
M=M+1                        // line 10
@LCL                         // line 11
D=M                          // line 12
@SP                          // line 13
A=M                          // line 14
M=D                          // line 15
@SP                          // line 16
M=M+1                        // line 17
@ARG                         // line 18
D=M                          // line 19
@SP                          // line 20
A=M                          // line 21
M=D                          // line 22
@SP                          // line 23
M=M+1                        // line 24
@THIS                        // line 25
D=M                          // line 26
@SP                          // line 27
A=M                          // line 28
M=D                          // line 29
@SP                          // line 30
M=M+1                        // line 31
@THAT                        // line 32
D=M                          // line 33
@SP                          // line 34
A=M                          // line 35
M=D                          // line 36
@SP                          // line 37
M=M+1                        // line 38
@SP                          // line 39
D=M                          // line 40
@5                           // line 41
D=D-A                        // line 42
@ARG                         // line 43
M=D                          // line 44
@SP                          // line 45
D=M                          // line 46
@LCL                         // line 47
M=D                          // line 48
@Sys.init                    // line 49
0;JMP                        // line 50
(Sys.init.1.return)

// ---------
// Class1.vm
// ---------

// function Class1.set 0
(Class1.set)
// push argument 0
@ARG                         // line 51
D=M                          // line 52
@0                           // line 53
D=D+A                        // line 54
A=D                          // line 55
D=M                          // line 56
@SP                          // line 57
A=M                          // line 58
M=D                          // line 59
@SP                          // line 60
M=M+1                        // line 61
// pop static 0
@Class1.vm.16                // line 62
D=A                          // line 63
@13                          // line 64
M=D                          // line 65
@SP                          // line 66
M=M-1                        // line 67
A=M                          // line 68
D=M                          // line 69
@13                          // line 70
A=M                          // line 71
M=D                          // line 72
// push argument 1
@ARG                         // line 73
D=M                          // line 74
@1                           // line 75
D=D+A                        // line 76
A=D                          // line 77
D=M                          // line 78
@SP                          // line 79
A=M                          // line 80
M=D                          // line 81
@SP                          // line 82
M=M+1                        // line 83
// pop static 1
@Class1.vm.17                // line 84
D=A                          // line 85
@13                          // line 86
M=D                          // line 87
@SP                          // line 88
M=M-1                        // line 89
A=M                          // line 90
D=M                          // line 91
@13                          // line 92
A=M                          // line 93
M=D                          // line 94
// push constant 0
@0                           // line 95
D=A                          // line 96
@SP                          // line 97
A=M                          // line 98
M=D                          // line 99
@SP                          // line 100
M=M+1                        // line 101
// return
@LCL                         // line 102
D=M                          // line 103
@endFrame                    // line 104
M=D                          // line 105
@5                           // line 106
D=D-A                        // line 107
A=D                          // line 108
D=M                          // line 109
@retAddr                     // line 110
M=D                          // line 111
@SP                          // line 112
M=M-1                        // line 113
A=M                          // line 114
D=M                          // line 115
@ARG                         // line 116
A=M                          // line 117
M=D                          // line 118
@ARG                         // line 119
D=M+1                        // line 120
@SP                          // line 121
M=D                          // line 122
@endFrame                    // line 123
M=M-1                        // line 124
A=M                          // line 125
D=M                          // line 126
@THAT                        // line 127
M=D                          // line 128
@endFrame                    // line 129
M=M-1                        // line 130
A=M                          // line 131
D=M                          // line 132
@THIS                        // line 133
M=D                          // line 134
@endFrame                    // line 135
M=M-1                        // line 136
A=M                          // line 137
D=M                          // line 138
@ARG                         // line 139
M=D                          // line 140
@endFrame                    // line 141
M=M-1                        // line 142
A=M                          // line 143
D=M                          // line 144
@LCL                         // line 145
M=D                          // line 146
@retAddr                     // line 147
A=M                          // line 148
0;JMP                        // line 149
// function Class1.get 0
(Class1.get)
// push static 0
@Class1.vm.16                // line 150
D=M                          // line 151
@SP                          // line 152
A=M                          // line 153
M=D                          // line 154
@SP                          // line 155
M=M+1                        // line 156
// push static 1
@Class1.vm.17                // line 157
D=M                          // line 158
@SP                          // line 159
A=M                          // line 160
M=D                          // line 161
@SP                          // line 162
M=M+1                        // line 163
// sub
@SP                          // line 164
M=M-1                        // line 165
A=M                          // line 166
D=M                          // line 167
@SP                          // line 168
M=M-1                        // line 169
A=M                          // line 170
M=M-D                        // line 171
@SP                          // line 172
M=M+1                        // line 173
// return
@LCL                         // line 174
D=M                          // line 175
@endFrame                    // line 176
M=D                          // line 177
@5                           // line 178
D=D-A                        // line 179
A=D                          // line 180
D=M                          // line 181
@retAddr                     // line 182
M=D                          // line 183
@SP                          // line 184
M=M-1                        // line 185
A=M                          // line 186
D=M                          // line 187
@ARG                         // line 188
A=M                          // line 189
M=D                          // line 190
@ARG                         // line 191
D=M+1                        // line 192
@SP                          // line 193
M=D                          // line 194
@endFrame                    // line 195
M=M-1                        // line 196
A=M                          // line 197
D=M                          // line 198
@THAT                        // line 199
M=D                          // line 200
@endFrame                    // line 201
M=M-1                        // line 202
A=M                          // line 203
D=M                          // line 204
@THIS                        // line 205
M=D                          // line 206
@endFrame                    // line 207
M=M-1                        // line 208
A=M                          // line 209
D=M                          // line 210
@ARG                         // line 211
M=D                          // line 212
@endFrame                    // line 213
M=M-1                        // line 214
A=M                          // line 215
D=M                          // line 216
@LCL                         // line 217
M=D                          // line 218
@retAddr                     // line 219
A=M                          // line 220
0;JMP                        // line 221

// ------
// Sys.vm
// ------

// function Sys.init 0
(Sys.init)
// push constant 6
@6                           // line 222
D=A                          // line 223
@SP                          // line 224
A=M                          // line 225
M=D                          // line 226
@SP                          // line 227
M=M+1                        // line 228
// push constant 8
@8                           // line 229
D=A                          // line 230
@SP                          // line 231
A=M                          // line 232
M=D                          // line 233
@SP                          // line 234
M=M+1                        // line 235
// call Class1.set 2
@Class1.set.1.return         // line 236
D=A                          // line 237
@SP                          // line 238
A=M                          // line 239
M=D                          // line 240
@SP                          // line 241
M=M+1                        // line 242
@LCL                         // line 243
D=M                          // line 244
@SP                          // line 245
A=M                          // line 246
M=D                          // line 247
@SP                          // line 248
M=M+1                        // line 249
@ARG                         // line 250
D=M                          // line 251
@SP                          // line 252
A=M                          // line 253
M=D                          // line 254
@SP                          // line 255
M=M+1                        // line 256
@THIS                        // line 257
D=M                          // line 258
@SP                          // line 259
A=M                          // line 260
M=D                          // line 261
@SP                          // line 262
M=M+1                        // line 263
@THAT                        // line 264
D=M                          // line 265
@SP                          // line 266
A=M                          // line 267
M=D                          // line 268
@SP                          // line 269
M=M+1                        // line 270
@SP                          // line 271
D=M                          // line 272
@7                           // line 273
D=D-A                        // line 274
@ARG                         // line 275
M=D                          // line 276
@SP                          // line 277
D=M                          // line 278
@LCL                         // line 279
M=D                          // line 280
@Class1.set                  // line 281
0;JMP                        // line 282
(Class1.set.1.return)
// pop temp 0
@5                           // line 283
D=A                          // line 284
@13                          // line 285
M=D                          // line 286
@SP                          // line 287
M=M-1                        // line 288
A=M                          // line 289
D=M                          // line 290
@13                          // line 291
A=M                          // line 292
M=D                          // line 293
// push constant 23
@23                          // line 294
D=A                          // line 295
@SP                          // line 296
A=M                          // line 297
M=D                          // line 298
@SP                          // line 299
M=M+1                        // line 300
// push constant 15
@15                          // line 301
D=A                          // line 302
@SP                          // line 303
A=M                          // line 304
M=D                          // line 305
@SP                          // line 306
M=M+1                        // line 307
// call Class2.set 2
@Class2.set.1.return         // line 308
D=A                          // line 309
@SP                          // line 310
A=M                          // line 311
M=D                          // line 312
@SP                          // line 313
M=M+1                        // line 314
@LCL                         // line 315
D=M                          // line 316
@SP                          // line 317
A=M                          // line 318
M=D                          // line 319
@SP                          // line 320
M=M+1                        // line 321
@ARG                         // line 322
D=M                          // line 323
@SP                          // line 324
A=M                          // line 325
M=D                          // line 326
@SP                          // line 327
M=M+1                        // line 328
@THIS                        // line 329
D=M                          // line 330
@SP                          // line 331
A=M                          // line 332
M=D                          // line 333
@SP                          // line 334
M=M+1                        // line 335
@THAT                        // line 336
D=M                          // line 337
@SP                          // line 338
A=M                          // line 339
M=D                          // line 340
@SP                          // line 341
M=M+1                        // line 342
@SP                          // line 343
D=M                          // line 344
@7                           // line 345
D=D-A                        // line 346
@ARG                         // line 347
M=D                          // line 348
@SP                          // line 349
D=M                          // line 350
@LCL                         // line 351
M=D                          // line 352
@Class2.set                  // line 353
0;JMP                        // line 354
(Class2.set.1.return)
// pop temp 0
@5                           // line 355
D=A                          // line 356
@13                          // line 357
M=D                          // line 358
@SP                          // line 359
M=M-1                        // line 360
A=M                          // line 361
D=M                          // line 362
@13                          // line 363
A=M                          // line 364
M=D                          // line 365
// call Class1.get 0
@Class1.get.1.return         // line 366
D=A                          // line 367
@SP                          // line 368
A=M                          // line 369
M=D                          // line 370
@SP                          // line 371
M=M+1                        // line 372
@LCL                         // line 373
D=M                          // line 374
@SP                          // line 375
A=M                          // line 376
M=D                          // line 377
@SP                          // line 378
M=M+1                        // line 379
@ARG                         // line 380
D=M                          // line 381
@SP                          // line 382
A=M                          // line 383
M=D                          // line 384
@SP                          // line 385
M=M+1                        // line 386
@THIS                        // line 387
D=M                          // line 388
@SP                          // line 389
A=M                          // line 390
M=D                          // line 391
@SP                          // line 392
M=M+1                        // line 393
@THAT                        // line 394
D=M                          // line 395
@SP                          // line 396
A=M                          // line 397
M=D                          // line 398
@SP                          // line 399
M=M+1                        // line 400
@SP                          // line 401
D=M                          // line 402
@5                           // line 403
D=D-A                        // line 404
@ARG                         // line 405
M=D                          // line 406
@SP                          // line 407
D=M                          // line 408
@LCL                         // line 409
M=D                          // line 410
@Class1.get                  // line 411
0;JMP                        // line 412
(Class1.get.1.return)
// call Class2.get 0
@Class2.get.1.return         // line 413
D=A                          // line 414
@SP                          // line 415
A=M                          // line 416
M=D                          // line 417
@SP                          // line 418
M=M+1                        // line 419
@LCL                         // line 420
D=M                          // line 421
@SP                          // line 422
A=M                          // line 423
M=D                          // line 424
@SP                          // line 425
M=M+1                        // line 426
@ARG                         // line 427
D=M                          // line 428
@SP                          // line 429
A=M                          // line 430
M=D                          // line 431
@SP                          // line 432
M=M+1                        // line 433
@THIS                        // line 434
D=M                          // line 435
@SP                          // line 436
A=M                          // line 437
M=D                          // line 438
@SP                          // line 439
M=M+1                        // line 440
@THAT                        // line 441
D=M                          // line 442
@SP                          // line 443
A=M                          // line 444
M=D                          // line 445
@SP                          // line 446
M=M+1                        // line 447
@SP                          // line 448
D=M                          // line 449
@5                           // line 450
D=D-A                        // line 451
@ARG                         // line 452
M=D                          // line 453
@SP                          // line 454
D=M                          // line 455
@LCL                         // line 456
M=D                          // line 457
@Class2.get                  // line 458
0;JMP                        // line 459
(Class2.get.1.return)
// label WHILE
(WHILE)
// goto WHILE
@WHILE                       // line 460
0;JMP                        // line 461

// ---------
// Class2.vm
// ---------

// function Class2.set 0
(Class2.set)
// push argument 0
@ARG                         // line 462
D=M                          // line 463
@0                           // line 464
D=D+A                        // line 465
A=D                          // line 466
D=M                          // line 467
@SP                          // line 468
A=M                          // line 469
M=D                          // line 470
@SP                          // line 471
M=M+1                        // line 472
// pop static 0
@Class2.vm.16                // line 473
D=A                          // line 474
@13                          // line 475
M=D                          // line 476
@SP                          // line 477
M=M-1                        // line 478
A=M                          // line 479
D=M                          // line 480
@13                          // line 481
A=M                          // line 482
M=D                          // line 483
// push argument 1
@ARG                         // line 484
D=M                          // line 485
@1                           // line 486
D=D+A                        // line 487
A=D                          // line 488
D=M                          // line 489
@SP                          // line 490
A=M                          // line 491
M=D                          // line 492
@SP                          // line 493
M=M+1                        // line 494
// pop static 1
@Class2.vm.17                // line 495
D=A                          // line 496
@13                          // line 497
M=D                          // line 498
@SP                          // line 499
M=M-1                        // line 500
A=M                          // line 501
D=M                          // line 502
@13                          // line 503
A=M                          // line 504
M=D                          // line 505
// push constant 0
@0                           // line 506
D=A                          // line 507
@SP                          // line 508
A=M                          // line 509
M=D                          // line 510
@SP                          // line 511
M=M+1                        // line 512
// return
@LCL                         // line 513
D=M                          // line 514
@endFrame                    // line 515
M=D                          // line 516
@5                           // line 517
D=D-A                        // line 518
A=D                          // line 519
D=M                          // line 520
@retAddr                     // line 521
M=D                          // line 522
@SP                          // line 523
M=M-1                        // line 524
A=M                          // line 525
D=M                          // line 526
@ARG                         // line 527
A=M                          // line 528
M=D                          // line 529
@ARG                         // line 530
D=M+1                        // line 531
@SP                          // line 532
M=D                          // line 533
@endFrame                    // line 534
M=M-1                        // line 535
A=M                          // line 536
D=M                          // line 537
@THAT                        // line 538
M=D                          // line 539
@endFrame                    // line 540
M=M-1                        // line 541
A=M                          // line 542
D=M                          // line 543
@THIS                        // line 544
M=D                          // line 545
@endFrame                    // line 546
M=M-1                        // line 547
A=M                          // line 548
D=M                          // line 549
@ARG                         // line 550
M=D                          // line 551
@endFrame                    // line 552
M=M-1                        // line 553
A=M                          // line 554
D=M                          // line 555
@LCL                         // line 556
M=D                          // line 557
@retAddr                     // line 558
A=M                          // line 559
0;JMP                        // line 560
// function Class2.get 0
(Class2.get)
// push static 0
@Class2.vm.16                // line 561
D=M                          // line 562
@SP                          // line 563
A=M                          // line 564
M=D                          // line 565
@SP                          // line 566
M=M+1                        // line 567
// push static 1
@Class2.vm.17                // line 568
D=M                          // line 569
@SP                          // line 570
A=M                          // line 571
M=D                          // line 572
@SP                          // line 573
M=M+1                        // line 574
// sub
@SP                          // line 575
M=M-1                        // line 576
A=M                          // line 577
D=M                          // line 578
@SP                          // line 579
M=M-1                        // line 580
A=M                          // line 581
M=M-D                        // line 582
@SP                          // line 583
M=M+1                        // line 584
// return
@LCL                         // line 585
D=M                          // line 586
@endFrame                    // line 587
M=D                          // line 588
@5                           // line 589
D=D-A                        // line 590
A=D                          // line 591
D=M                          // line 592
@retAddr                     // line 593
M=D                          // line 594
@SP                          // line 595
M=M-1                        // line 596
A=M                          // line 597
D=M                          // line 598
@ARG                         // line 599
A=M                          // line 600
M=D                          // line 601
@ARG                         // line 602
D=M+1                        // line 603
@SP                          // line 604
M=D                          // line 605
@endFrame                    // line 606
M=M-1                        // line 607
A=M                          // line 608
D=M                          // line 609
@THAT                        // line 610
M=D                          // line 611
@endFrame                    // line 612
M=M-1                        // line 613
A=M                          // line 614
D=M                          // line 615
@THIS                        // line 616
M=D                          // line 617
@endFrame                    // line 618
M=M-1                        // line 619
A=M                          // line 620
D=M                          // line 621
@ARG                         // line 622
M=D                          // line 623
@endFrame                    // line 624
M=M-1                        // line 625
A=M                          // line 626
D=M                          // line 627
@LCL                         // line 628
M=D                          // line 629
@retAddr                     // line 630
A=M                          // line 631
0;JMP                        // line 632