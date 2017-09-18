# CSAW 2017 pwn 100 scv

# 題目:


>                                         SCV
>            SCV is too hungry to mine the minerals. Can you give him some food?
>                                 nc pwn.chal.csaw.io 3764

>[scv](scv)

>[ibc-2.23.so](ibc-2.23.so)


呢題有少少煩,不過唔難

Checksec:

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

```
IO dump:

```
-------------------------
[*]SCV GOOD TO GO,SIR....
-------------------------
1.FEED SCV....
2.REVIEW THE FOOD....
3.MINE MINERALS....
-------------------------
>>

```

有3個function:

1.入buffer

2.print buffer

3.exit


Ida code (由於好多廢話,所以淨係留重點)

```C++
                .
                .
 char buf; // [sp+10h] [bp-B0h]@6
                .
                .

   v23 = read(0, &buf, 248uLL);             .

```

有用嘅其實只有一/兩句,其他都係廢話

呢兩句identify 左有buffer overflow, buffer只有176 byte,但係可以讀248,仲唔死

asm code:

```asm
.text:0000000000400A96 buf             = byte ptr -0B0h
.text:0000000000400A96 var_8           = qword ptr -8
.text:0000000000400A96
.text:0000000000400A96                 push    rbp
.text:0000000000400A97                 mov     rbp, rsp
.text:0000000000400A9A                 sub     rsp, 0C0h
.text:0000000000400AA1                 mov     rax, fs:28h
.text:0000000000400AAA                 mov     [rbp+var_8], rax
.text:0000000000400AAE                 xor     eax, eax
.text:0000000000400AB0                 mov     rax, cs:stdout

```

我地知道canary 係rbp-8, 只要leak到canary,就可以任意寫return address, get shell

經過少少測試之後,會發現print buffer function會print多左8個位 or until \x00

我地知道嘅尾數係\x00, 所以我地只要寫到尾數做其他野就leak到canary

leak canary payload= payload='b'*167+'a'+'g'

只要將leak到嘅canary減0x67,就等於canary number




