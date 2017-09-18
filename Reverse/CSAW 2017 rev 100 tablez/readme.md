# CSAW 2017 rev 100 tablez

# 題目:


>                                         tablEZ
>Bobby was talking about tables a bunch, so I made some table stuff. I think this is what he was talking about...
>
>[tablez](tablez)


呢題係今次嘅嘅sanity check, 其實唔難

IDA Pro main:

```C++
  s[strlen(s) - 1] = 0;
  v6 = strlen(s);
  for ( i = 0LL; i < v6; ++i )
    s[i] = get_tbl_entry((unsigned int)s[i]);
  if ( v6 == 37 )
  {
    if ( !strncmp(s, s2, 0x26uLL) )
    {
      puts("CORRECT <3");
      result = 0;
    }
```
題目就係入支flag落去,做transformation, 再同正確嘅flag transformation 對比 

transformation function:

```C++
__int64 __fastcall get_tbl_entry(char a1)
{
  unsigned __int64 i; // [sp+Ch] [bp-8h]@1

  for ( i = 0LL; i <= 0xFE; ++i )
  {
    if ( a1 == *((_BYTE *)&trans_tbl + 2 * i) )
      return byte_201281[2 * i];
  }
  return 0LL;
}
```

算法好簡單,只要將個byte table dump 出黎 就完成左part 1

之後係之前set breakpoint (0x9F7), 抄埋 rcx  (正確嘅flag transformation )

strncmp assmebly:

```asm
.text:00000000000009DE loc_9DE:                                ; CODE XREF: main+129j
.text:00000000000009DE                 lea     rcx, [rbp+s2]
.text:00000000000009E5                 lea     rax, [rbp+s]
.text:00000000000009EC                 mov     edx, 26h        ; n
.text:00000000000009F1                 mov     rsi, rcx        ; s2
.text:00000000000009F4                 mov     rdi, rax        ; s1
.text:00000000000009F7                 call    _strncmp
.text:00000000000009FC                 test    eax, eax
.text:00000000000009FE                 jnz     short loc_A13
.text:0000000000000A00                 lea     rdi, aCorrect3  ; "CORRECT <3"
.text:0000000000000A07                 call    _puts
.text:0000000000000A0C                 mov     eax, 0
.text:0000000000000A11                 jmp     short loc_A24
```

有table+result之後,再python implement 1次佢個transfomation algorithm就可以


由於作者唔識打code同睇assembly,所以就求其打左個basic search,再返gdb人手check transformation result ~_~



